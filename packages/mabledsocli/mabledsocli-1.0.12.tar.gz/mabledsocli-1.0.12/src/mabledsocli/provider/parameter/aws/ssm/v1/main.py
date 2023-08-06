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

    def list(self, project, application, stage, uninherited):
        parameters = load_context_ssm_parameters(project, application, stage, ['String'], prefix=_settings['prefix'], uninherited=uninherited)
        result = {'Parameters': []}
        for key, details in parameters.items():
            result['Parameters'].append({
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
                raise DSOException(f"Revision '{revision}' not found for parameter '{key}' in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
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
