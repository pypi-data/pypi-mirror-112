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
from mabledsocli.parameters import ParameterProvider
from mabledsocli.stages import Stages
from mabledsocli.constants import *
from mabledsocli.dict_utils import set_dict_value


_default_spec = {
}

def get_default_spec():
    return _default_spec.copy()


session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)


class AwsSsmTemplateProvider(ParameterProvider):

    def __init__(self):
        super().__init__('template/aws/ssm/v1')

###--------------------------------------------------------------------------------------------

    def get_template_prefix(self, project, application, key=None):
        result = "/dso/templates"
        result += f"/{project}"
        ### every application must belong to a project, no application overrides allowed in the default project
        if not project == 'default':
            result += f"/{application}"
        else:
            result += "/default"
        # result += f"/{stage}"
        if key:
            result += f"/{key}"
        return result

###--------------------------------------------------------------------------------------------
    ### AWS SSM Parameyer store does not allow {{}}
    def escape_curly_brackets(self, contents):
        return contents.replace('{{', r'\{\{').replace('}}', r'\}\}')

###--------------------------------------------------------------------------------------------

    def unescape_curly_brackets(self, contents):
        return contents.replace(r'\{\{', '{{').replace(r'\}\}', '}}')

###--------------------------------------------------------------------------------------------

    def assert_no_scope_overwrites(self, project, application, key):
        """
            check if a template will overwrite parent or childern parameters (with the same scopes) in the same stage (always uninherited)
            e.g.: 
                template a.b.c would overwrite a.b (super scope)
                template a.b would overwrite a.b.c (sub scope)
        """
        Logger.debug(f"Checking template overwrites: project={project}, application={application}, key={key}")
        
        ### check children templates
        path = self.get_template_prefix(project, application, key)
        # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String']},{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Template key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other templates in '{0}.*' scope if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

        ### check parent templates
        scopes = key.split('.')
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_template_prefix(project, application, subKey)
            Logger.debug(f"Describing templates: path={path}")
            # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0:
                raise DSOException("Template key '{0}' is not allowed in the given context becasue it would overwrite template '{1}'.".format(key, subKey))

###--------------------------------------------------------------------------------------------

    def locate_template(self, project, application, key, uninherited=False):
        Logger.debug(f"Locating SSM template: project={project}, application={application}, key={key}")
        paths = self.get_hierachy_paths(project, application, key, uninherited)
        # Logger.debug(f"SSM paths to search in order: {paths}")
        for path in paths:
            Logger.debug(f"Describing SSM templates: path={path}")
            # result = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0: return response['Parameters']
        return []

###--------------------------------------------------------------------------------------------

    def load_ssm_path(self, templates, path, recurisve=True):
        Logger.debug(f"Loading SSM templates: path={path}")
        p = ssm.get_paginator('get_parameters_by_path')
        paginator = p.paginate(Path=path, Recursive=recurisve, ParameterFilters=[{'Key': 'Type','Values': ['StringList']}]).build_full_result()
        for template in paginator['Parameters']:
            key = template['Name'][len(path)+1:]
            if key in templates:
                Logger.warn("Inherited template '{0}' overridden.".format(key))
            templates[key] = {'Contents': template['Value'], 
                                'Path': template['Name'],
                                'Version': template['Version'],
                                'Date': template['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                            }
        return templates

###--------------------------------------------------------------------------------------------

    def get_hierachy_paths(self, project, application, key, uninherited):
        paths = []
        if uninherited:
            paths.append(self.get_template_prefix(project, application, key))
        else:
            ### Add the global context: /dso/default/default
            paths.append(self.get_template_prefix('default', 'default', key))
            if not project == 'default':
                ### Add the project context: /dso/project/default
                paths.append(self.get_template_prefix(project, 'default', key))
                if not application == 'default':
                    ### Add the application context: /dso/project/application
                    paths.append(self.get_template_prefix(project, application, key))

        return paths

###--------------------------------------------------------------------------------------------

    def list(self, project, application, uninherited):
        ### construct search path in hierachy with no key specified
        paths = list(self.get_hierachy_paths(project, application, None, uninherited))
        # Logger.debug(f"SSM paths to search in order: {paths}")
        templates = {}
        for path in paths:
            self.load_ssm_path(templates, path)

        result = {'Templates': []}
        for item in templates.items():
            result['Templates'].append({'Key': item[0], 
                                        # 'Contents': item[1]['Value'], 
                                        'Path': item[1]['Path'],
                                        'RevisionId': str(item[1]['Version']),
                                        'Date': item[1]['Date'],
                                        })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, key, contents):
        if len(contents) > 4096:
            raise DSOException(f"This template provider does not support templates larger than 4KB.")
        self.assert_no_scope_overwrites(project, application, key)
        found = self.locate_template(project, application, key, uninherited=True)
        if found and not found[0]['Type'] == 'StringList':
            raise DSOException(f"Failed to add template '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}")
        path = self.get_template_prefix(project, application, key=key)
        Logger.info(f"Adding SSM template: path={path}")
        escapedContents = self.escape_curly_brackets(contents)
        response = ssm.put_parameter(Name=path, Value=escapedContents, Type='StringList', Overwrite=True)
        return {'Key': key,
                # 'Contents': contents,
                'Path': path,
                'RevisionId': str(response['Version']),
                }

###--------------------------------------------------------------------------------------------

    def get(self, project, application, key, revision=None):
        found = self.locate_template(project, application, key)
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        else:
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        Logger.info(f"Getting SSM template: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        templates = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(templates[0]['Version']),
                    'Key': key, 
                    'Contents': self.unescape_curly_brackets(templates[0]['Value']),
                    'Path': found[0]['Name'],
                    'Date': templates[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': templates[0]['LastModifiedUser'],
                    }
        else:
            ### get specific revision
            templates = [x for x in templates if str(x['Version']) == revision]
            if not templates:
                raise DSOException(f"Revision '{revision}' not found in the given context: project={project}, application={application}, key={key}")
            result = {
                    'RevisionId': str(templates[0]['Version']),
                    'Key': key, 
                    'Contents': self.unescape_curly_brackets(templates[0]['Value']),
                    'Path': found[0]['Name'],
                    'Date': templates[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'User': templates[0]['LastModifiedUser'],
                    }

        return result

###--------------------------------------------------------------------------------------------

    def history(self, project, application, key):
        found = self.locate_template(project, application, key)
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        else:
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        Logger.info(f"Getting SSM template: path={found[0]['Name']}")
        response = ssm.get_parameter_history(Name=found[0]['Name'])
        parameters = sorted(response['Parameters'], key=lambda x: x['Version'], reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(template['Version']),
                'Key': key,
                # 'Contents': self.unescape_curly_brackets(template['Value']),
                'Path': found[0]['Name'],
                'Date': template['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'User': template['LastModifiedUser'],
            } for template in parameters]
        }

        return result

###--------------------------------------------------------------------------------------------

    def delete(self, project, application, key):
        ### only parameters owned by the stage can be deleted, hence uninherited=True
        found = self.locate_template(project, application, key, uninherited=True)
        if not found:
            raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one template found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] == 'StringList':
                raise DSOException(f"Template '{key}' not found in the given context: project={project}, application={application}")
        Logger.info(f"Deleting SSM template: path={found[0]['Name']}")
        response = ssm.delete_parameter(Name=found[0]['Name'])
        return {
                'Key': key, 
                'Path': found[0]['Name'],
                }

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

Providers.register(AwsSsmTemplateProvider())
