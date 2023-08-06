import re
import boto3
from mabledsocli.exceptions import DSOException
from mabledsocli.logger import Logger
from mabledsocli.config import Configs
from mabledsocli.providers import Providers
from mabledsocli.templates import TemplateProvider
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
    'id': 'template/aws/ssm/v1',
    'prefix': '/dso/templates',
}

session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)


class AwsSsmTemplateProvider(TemplateProvider):

    def __init__(self):
        super().__init__(_settings['id'])

###--------------------------------------------------------------------------------------------

    def get_prefix(self, project, application, stage, key=None):
        return _settings['prefix'] + Contexts.encode_context_path(project, application, stage, key)


###--------------------------------------------------------------------------------------------
    ### AWS SSM Parameyer store does not allow {{}}
    def escape_curly_brackets(self, contents):
        return contents.replace('{{', r'\{\{').replace('}}', r'\}\}')

###--------------------------------------------------------------------------------------------

    def unescape_curly_brackets(self, contents):
        return contents.replace(r'\{\{', '{{').replace(r'\}\}', '}}')

###--------------------------------------------------------------------------------------------

    def list(self, project, application, stage, uninherited):
        templates = load_context_ssm_parameters(project, application, stage, ['StringList'], prefix=_settings['prefix'], uninherited=uninherited)
        result = {'Templates': []}
        for key, details in templates.items():
            result['Templates'].append({
                                    'Key': key, 
                                    # 'Contents': details['Value'], 
                                    'Scope': details['Scope'],
                                    'RevisionId': str(details['Version']),
                                    'Date': details['Date'],
                                    'Version': details['Version'],
                                    'Path': details['Path'],
                                    })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, stage, key, contents):
        if len(contents) > 4096:
            raise DSOException(f"This template provider does not support templates larger than 4KB.")
        assert_ssm_parameter_no_namespace_overwrites(project, application, stage, key)
        Logger.debug(f"Locating SSM template: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
        if found and not found[0]['Type'] == 'StringList':
            raise DSOException(f"Failed to add template '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        path = self.get_prefix(project, application, stage, key)
        Logger.info(f"Adding SSM template: path={path}")
        response = ssm.put_parameter(Name=path, Value=self.escape_curly_brackets(contents), Type='StringList', Overwrite=True)
        return {
            'Key': key,
                # 'Contents': contents,
                'Scope': Contexts.translate_context(project, application, stage),
                'RevisionId': str(response['Version']),
                'Version': response['Version'],
                'Path': path,
                }

###--------------------------------------------------------------------------------------------

    def get(self, project, application, stage, key, revision=None):
        Logger.debug(f"Locating SSM template: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM template: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        templates = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(templates[0]['Version']),
                    'Key': key, 
                    'Contents': self.unescape_curly_brackets(templates[0]['Value']),
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': templates[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': templates[0]['LastModifiedUser'],
                    'Version': templates[0]['Version'],
                    'Path': found[0]['Name'],
                    }
        else:
            ### get specific revision
            templates = [x for x in templates if str(x['Version']) == revision]
            if not templates:
                raise DSOException(f"Revision '{revision}' not found for template '{key}' in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
            result = {
                    'RevisionId': str(templates[0]['Version']),
                    'Key': key, 
                    'Contents': self.unescape_curly_brackets(templates[0]['Value']),
                    'Scope': Contexts.translate_context(project, application, stage),
                    'Date': templates[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': templates[0]['LastModifiedUser'],
                    'Version': templates[0]['Version'],
                    'Path': found[0]['Name'],
                    }

        return result

###--------------------------------------------------------------------------------------------

    def history(self, project, application, stage, key):
        Logger.debug(f"Locating SSM template: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'])
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM template: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        parameters = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(template['Version']),
                'Key': key,
                # 'Contents': self.unescape_curly_brackets(template['Value']),
                'Scope': Contexts.translate_context(project, application, stage),
                'Date': template['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'User': template['LastModifiedUser'],
                'Version': template['Version'],
                'Path': found[0]['Name'],
            } for template in parameters]
        }

        return result

###--------------------------------------------------------------------------------------------

    def delete(self, project, application, stage, key):
        Logger.debug(f"Locating SSM template: project={project}, application={application}, stage={stage}, key={key}")
        ### only parameters owned by the stage can be deleted, hence uninherited=True
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=_settings['prefix'], uninherited=True)
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one template found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Deleting SSM template: path={found[0]['Name']}")
        response = ssm.delete_parameter(Name=found[0]['Name'])
        return {
                'Key': key, 
                'Scope': Contexts.translate_context(project, application, stage),
                'Path': found[0]['Name'],
                }

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

Providers.register(AwsSsmTemplateProvider())
