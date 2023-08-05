import re
import boto3
from mabledsocli.exceptions import DSOException
from mabledsocli.logger import Logger
from mabledsocli.config import Configs
from mabledsocli.providers import Providers
from mabledsocli.parameters import ParameterProvider
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
    'id': 'parameter/aws/ssm/v1',
    'prefix': '/dso/parameters',
}

session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)


class AwsSsmParameterProvider(ParameterProvider):

    def __init__(self):
        super().__init__(_settings['id'])

###--------------------------------------------------------------------------------------------

    def get_prefix(self, project, application, stage, key=None):
        return _settings['prefix'] + Contexts.encode_context_path(project, application, stage, key)

###--------------------------------------------------------------------------------------------

    def assert_no_scope_overwrites(self, project, application, stage, key):
        """
            check if a parameter will overwrite parent or childern parameters (with the same scopes) in the same stage (always uninherited)
            e.g.: 
                parameter a.b.c would overwrite a.b (super scope)
                parameter a.b would overwrite a.b.c (sub scope)
        """
        Logger.debug(f"Checking parameter overwrites: project={project}, application={application}, stage={stage}, key={key}")
        
        ### check children parameters
        path = self.get_prefix(project, application, stage, key)
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other parameters in '{0}.*' scope if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

        ### check parent parameters
        scopes = key.split('.')
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_prefix(project, application, stage, subKey)
            Logger.debug(f"Describing parameters: path={path}")
            # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0:
                raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite parameter '{1}'.".format(key, subKey))

###--------------------------------------------------------------------------------------------

    def list(self, project, application, stage, uninherited):
        # ### construct search path in hierachy with no key specified
        # paths = Contexts.get_hierachy_context_paths(project, application, stage, key=None, prefix=_settings['prefix'], allow_stages=True, uninherited=uninherited)
        # # Logger.debug(f"SSM paths to search in order: {paths}")
        # parameters = {}
        # for path in paths:
        #     Logger.debug(f"Loading SSM parameters: path={path}")
        #     load_ssm_path(parameters, path, ['String'], _settings['prefix'])
        parameters = load_ssm_parameters(project, application, stage, ['String'], prefix=_settings['prefix'], uninherited=uninherited)
        result = {'Parameters': []}
        for item in parameters.items():
            result['Parameters'].append({
                                    'Key': item[0], 
                                    'Value': item[1]['Value'], 
                                    'Scope': item[1]['Scope'],
                                    'RevisionId': str(item[1]['Version']),
                                    'Date': item[1]['Date'],
                                    'Version': item[1]['Version'],
                                    'Path': item[1]['Path'],
                                    })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, stage, key, value):
        self.assert_no_scope_overwrites(project, application, stage, key)
        Logger.debug(f"Locating SSM parameter: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
        if found and not found[0]['Type'] == 'String':
            raise DSOException(f"Failed to add parameter '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        path = self.get_prefix(project, application, stage=stage, key=key)
        Logger.info(f"Adding SSM parameter: path={path}")
        response = ssm.put_parameter(Name=path, Value=value, Type='String', Overwrite=True)
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
        Logger.debug(f"Locating SSM parameter: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
        if not found:
            raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'String':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM parameter: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        parameters = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(parameters[0]['Version']),
                    'Key': key, 
                    'Value': parameters[0]['Value'],
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': parameters[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': parameters[0]['LastModifiedUser'],
                    'Version': parameters[0]['Version'],
                    'Path': found[0]['Name'],
                    }
        else:
            ### get specific revision
            parameters = [x for x in parameters if str(x['Version']) == revision]
            if not parameters:
                raise DSOException(f"Revision '{revision}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
            result = {
                    'RevisionId':str(parameters[0]['Version']),
                    'Key': key, 
                    'Value': parameters[0]['Value'],
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': parameters[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': parameters[0]['LastModifiedUser'],
                    'Version': parameters[0]['Version'],
                    'Path': found[0]['Name'],
                    }

        return result

###--------------------------------------------------------------------------------------------

    def history(self, project, application, stage, key):
        Logger.debug(f"Locating SSM parameter: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
        if not found:
            raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'String':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM parameter: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        parameters = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(parameter['Version']),
                'Key': key,
                'Value': parameter['Value'],
                'Scope': Contexts.translate_context(project, application, stage),
                'Date': parameter['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'User': parameter['LastModifiedUser'],
                'Version': parameter['Version'],
                'Path': found[0]['Name'],
            } for parameter in parameters]
        }

        return result

###--------------------------------------------------------------------------------------------

    def delete(self, project, application, stage, key):
        Logger.debug(f"Locating SSM parameter: project={project}, application={application}, stage={stage}, key={key}")
        ### only parameters owned by the context can be deleted, hence uninherited=True
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
        if not found:
            raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one parameter found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] == 'String':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Deleting SSM parameter: path={found[0]['Name']}")
        ssm.delete_parameter(Name=found[0]['Name'])
        return {
                'Key': key, 
                'Scope': Contexts.translate_context(project, application, stage),
                'Path': found[0]['Name'],
                }

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

Providers.register(AwsSsmParameterProvider())
