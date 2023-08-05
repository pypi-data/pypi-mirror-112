import os
import re
import yaml
import json
import pathlib
import numbers
import boto3
from botocore.exceptions import ClientError
from mabledsocli.exceptions import DSOException
from mabledsocli.logger import Logger
from mabledsocli.config import Configs
from mabledsocli.providers import Providers
from mabledsocli.secrets import SecretProvider
from mabledsocli.stages import Stages
from mabledsocli.constants import *
from mabledsocli.dict_utils import set_dict_value
from mabledsocli.contexts import Contexts


_default_spec = {
}

def get_default_spec():
    return _default_spec.copy()


session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)


class AwsSsmSecretProvider(SecretProvider):

    def __init__(self):
        super().__init__('secret/aws/ssm/v1')

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    def get_secret_prefix(self, project, application, stage, key=None):
        result = "/dso/secrets"
        result += Contexts.encode_context_path(project, application, stage)
        if key:
            result += f"/{key}"
        return result

###--------------------------------------------------------------------------------------------

    def assert_no_scope_overwrites(self, project, application, stage, key):
        """
            check if a secret will overwrite parent or childern secrets (with the same scopes) in the same stage (always uninherited)
            e.g.: 
                secret a.b.c would overwrite a.b (super scope)
                secret a.b would overwrite a.b.c (sub scope)
        """
        Logger.debug(f"Checking secret overwrites: project={project}, application={application}, stage={stage}, key={key}")
        
        ### check children secrets
        path = self.get_secret_prefix(project, application, stage, key)
        # secrets = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['SecureString']},{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Secret key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other secrets in '{0}.*' scope if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

        ### check parent secrets
        scopes = key.split('.')
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_secret_prefix(project, application, stage, subKey)
            Logger.debug(f"Describing secrets: path={path}")
            # secrets = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['SecureString']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0:
                raise DSOException("Secret key '{0}' is not allowed in the given context becasue it would overwrite secret '{1}'.".format(key, subKey))

###--------------------------------------------------------------------------------------------

    def locate_secret(self, project, application, stage, key, uninherited=False):
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        paths = self.get_hierachy_paths(project, application, stage, key, uninherited)
        # Logger.debug(f"SSM paths to search in order: {paths}")
        for path in paths:
            Logger.debug(f"Describing SSM secrets: path={path}")
            # result = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['SecureString']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0: return response['Parameters']
        return []

###--------------------------------------------------------------------------------------------

    def load_ssm_path(self, secrets, path, decrypt, recurisve=True):
        Logger.debug(f"Loading SSM secrets: path={path}")
        project, application, stage = Contexts.decode_context_path(path[len('/dso/parameters'):])
        p = ssm.get_paginator('get_parameters_by_path')
        paginator = p.paginate(Path=path, Recursive=recurisve, WithDecryption=decrypt, ParameterFilters=[{'Key': 'Type','Values': ['SecureString']}]).build_full_result()
        for secret in paginator['Parameters']:
            key = secret['Name'][len(path)+1:]
            value = secret['Value']
            if key in secrets:
                Logger.warn("Inherited secret '{0}' overridden.".format(key))
            secrets[key] = {
                            'Value': secret['Value'], 
                            'Origin': Contexts.translate_context(project, application, stage),
                            'Path': secret['Name'],
                            'Version': secret['Version'],
                            'Date': secret['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                            }
        return secrets

###--------------------------------------------------------------------------------------------

    def get_hierachy_paths(self, project, application, stage, key, uninherited):
        paths = []
        if uninherited:
            paths.append(self.get_secret_prefix(project, application, stage, key))
        else:
            ### Add the global context: /dso/default/default/default/0
            paths.append(self.get_secret_prefix('default', 'default', 'default/0', key))
            if not Stages.is_default(stage):
                ### Add global stage context
                paths.append(self.get_secret_prefix('default', 'default', Stages.get_stage_default_env(stage), key))
                ### Add global numbered stage context
                if not Stages.is_stage_default_env(stage):
                    paths.append(self.get_secret_prefix('default', 'default', stage, key))

            if not project == 'default':
                ### Add the project context: /dso/project/default/default/0
                paths.append(self.get_secret_prefix(project, 'default', 'default/0', key))
                if not Stages.is_default(stage):
                    ### Add the project stage context: /dso/project/default/stage/0
                    paths.append(self.get_secret_prefix(project, 'default', Stages.get_stage_default_env(stage), key))
                    ### Add the project numbered stage context: /dso/project/default/stage/env
                    if not Stages.is_stage_default_env(stage):
                        paths.append(self.get_secret_prefix(project, 'default', stage, key))
                
                if not application == 'default':
                    ### Add the application context: /dso/project/application/default/0
                    paths.append(self.get_secret_prefix(project, application, 'default/0', key))
                    if not Stages.is_default(stage):
                        ### Add the project stage context: /dso/project/application/stage/0
                        paths.append(self.get_secret_prefix(project, application, Stages.get_stage_default_env(stage), key))
                        ### Add the application numbered stage context: /dso/project/application/stage/env
                        if not Stages.is_stage_default_env(stage):
                            paths.append(self.get_secret_prefix(project, application, stage, key))

        return paths

###--------------------------------------------------------------------------------------------

    def list(self, project, application, stage, uninherited, decrypt):
        ### construct search path in hierachy with no key specified
        paths = list(self.get_hierachy_paths(project, application, stage, None, uninherited))
        # Logger.debug(f"SSM paths to search in order: {paths}")
        secrets = {}
        for path in paths:
            self.load_ssm_path(secrets, path, decrypt)

        result = {'Secrets': []}
        for item in secrets.items():
            result['Secrets'].append({'Key': item[0], 
                                        'Value': item[1]['Value'], 
                                        'Origin': item[1]['Origin'],
                                        'Path': item[1]['Path'],
                                        'RevisionId': str(item[1]['Version']),
                                        'Date': item[1]['Date'],
                                        # 'Version': item[1]['Version'],
                                        })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, stage, key, value):
        self.assert_no_scope_overwrites(project, application, stage, key)
        found = self.locate_secret(project, application, stage, key, uninherited=True)
        if found and not found[0]['Type'] == 'SecureString':
            raise DSOException(f"Failed to add secret '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        path = self.get_secret_prefix(project, application, stage=stage, key=key)
        Logger.info(f"Adding SSM secret: path={path}")
        response = ssm.put_parameter(Name=path, Value=value, Type='SecureString', Overwrite=True)
        return {'Key': key, 
                'Value': value,
                'Origin': Contexts.translate_context(project, application, stage),
                'Path': path,
                'RevisionId': str(response['Version']),
                # 'Version': response['Version'],
                }

###--------------------------------------------------------------------------------------------

    def get(self, project, application, stage, key, revision=None):
        found = self.locate_secret(project, application, stage, key)
        if not found:
            raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'SecureString':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM secret: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'], WithDecryption=True)
        secrets = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(secrets[0]['Version']),
                    'Key': key, 
                    'Value': secrets[0]['Value'],
                    'Origin': Contexts.translate_context(project, application, stage),
                    'Path': found[0]['Name'],
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': secrets[0]['LastModifiedUser'],
                    # 'Version': secrets[0]['Version'],
                    }
        else:
            ### get specific revision
            secrets = [x for x in secrets if str(x['Version']) == revision]
            if not secrets:
                raise DSOException(f"Revision '{revision}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
            result = {
                    'RevisionId': str(secrets[0]['Version']),
                    'Key': key, 
                    'Value': secrets[0]['Value'],
                    'Origin': Contexts.translate_context(project, application, stage),
                    'Path': found[0]['Name'],
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': secrets[0]['LastModifiedUser'],
                    # 'Version': secrets[0]['Version'],
                    }

        return result

###--------------------------------------------------------------------------------------------

    def history(self, project, application, stage, key):
        found = self.locate_secret(project, application, stage, key)
        if not found:
            raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'SecureString':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM secret: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'], WithDecryption=True)
        secrets = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(secret['Version']),
                'Key': key,
                'Value': secret['Value'],
                'Origin': Contexts.translate_context(project, application, stage),
                'Path': found[0]['Name'],
                'Date': secret['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'User': secret['LastModifiedUser'],
                # 'Version': secret['Version'],
            } for secret in secrets]
        }

        return result

###--------------------------------------------------------------------------------------------

    def delete(self, project, application, stage, key):
        ### only secrets owned by the stage can be deleted, hence uninherited=True
        found = self.locate_secret(project, application, stage, key, uninherited=True)
        if not found:
                raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one secret found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] == 'SecureString':
                raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Deleting SSM secret: path={found[0]['Name']}")
        ssm.delete_parameter(Name=found[0]['Name'])
        return {
                'Key': key, 
                'Origin': Contexts.translate_context(project, application, stage),
                'Path': found[0]['Name'],
                }

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

Providers.register(AwsSsmSecretProvider())
