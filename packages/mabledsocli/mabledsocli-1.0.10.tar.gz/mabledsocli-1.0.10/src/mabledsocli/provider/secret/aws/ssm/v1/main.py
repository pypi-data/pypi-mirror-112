import re
import boto3
from mabledsocli.exceptions import DSOException
from mabledsocli.logger import Logger
from mabledsocli.config import Configs
from mabledsocli.providers import Providers
from mabledsocli.secrets import SecretProvider
from mabledsocli.stages import Stages
from mabledsocli.constants import *
from mabledsocli.dict_utils import set_dict_value
from mabledsocli.contexts import Contexts
from mabledsocli.aws_utils import *


_default_spec = {
}

def get_default_spec():
    return _default_spec.copy()

_settings = {
    'id': 'secret/aws/ssm/v1',
    'prefix': '/dso/secrets',
}


session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)


class AwsSsmSecretProvider(SecretProvider):

    def __init__(self):
        super().__init__(_settings['id'])

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    def get_prefix(self, project, application, stage, key=None):
        return _settings['prefix'] + Contexts.encode_context_path(project, application, stage, key)


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
        path = self.get_prefix(project, application, stage, key)
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Secret key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other secrets in '{0}.*' scope if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

        ### check parent secrets
        scopes = key.split('.')
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_prefix(project, application, stage, subKey)
            Logger.debug(f"Describing secrets: path={path}")
            # secrets = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['SecureString']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0:
                raise DSOException("Secret key '{0}' is not allowed in the given context becasue it would overwrite secret '{1}'.".format(key, subKey))

###--------------------------------------------------------------------------------------------

    def list(self, project, application, stage, uninherited, decrypt):
        secrets = load_context_ssm_parameters(project, application, stage, ['SecureString'], prefix=_settings['prefix'], uninherited=uninherited, decrypt=decrypt)
        result = {'Secrets': []}
        for key, details in secrets.items():
            result['Secrets'].append({
                                'Key': key, 
                                'Value': details['Value'], 
                                'Scope': details['Scope'],
                                'RevisionId': str(details['Version']),
                                'Date': details['Date'],
                                'Version': details['Version'],
                                'Path': details['Path'],
                                })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, stage, key, value):
        assert_ssm_parameter_no_namespace_overwrites(project, application, stage, key)
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
        if found and not found[0]['Type'] == 'SecureString':
            raise DSOException(f"Failed to add secret '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        path = self.get_prefix(project, application, stage=stage, key=key)
        Logger.info(f"Adding SSM secret: path={path}")
        response = ssm.put_parameter(Name=path, Value=value, Type='SecureString', Overwrite=True)
        return {
                'Key': key, 
                'Value': value,
                'Scope': Contexts.translate_context(project, application, stage),
                'RevisionId': str(response['Version']),
                'Version': response['Version'],
                'Path': path,
                }

###--------------------------------------------------------------------------------------------

    def get(self, project, application, stage, key, revision=None):
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
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
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': secrets[0]['LastModifiedUser'],
                    'Version': secrets[0]['Version'],
                    'Path': found[0]['Name'],
                    }
        else:
            ### get specific revision
            secrets = [x for x in secrets if str(x['Version']) == revision]
            if not secrets:
                raise DSOException(f"Revision '{revision}' not found for secret '{key}' in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
            result = {
                    'RevisionId': str(secrets[0]['Version']),
                    'Key': key, 
                    'Value': secrets[0]['Value'],
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': secrets[0]['LastModifiedUser'],
                    'Version': secrets[0]['Version'],
                    'Path': found[0]['Name'],
                    }

        return result

###--------------------------------------------------------------------------------------------

    def history(self, project, application, stage, key):
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
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
                'Scope': Contexts.translate_context(project, application, stage),
                'Date': secret['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'User': secret['LastModifiedUser'],
                'Version': secret['Version'],
                'Path': found[0]['Name'],
            } for secret in secrets]
        }

        return result

###--------------------------------------------------------------------------------------------

    def delete(self, project, application, stage, key):
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        ### only secrets owned by the context can be deleted, hence uninherited=True
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
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
                'Scope': Contexts.translate_context(project, application, stage),
                'Path': found[0]['Name'],
                }

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

Providers.register(AwsSsmSecretProvider())
