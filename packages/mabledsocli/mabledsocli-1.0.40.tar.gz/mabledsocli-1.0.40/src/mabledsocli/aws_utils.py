import boto3
from .contexts import Contexts
from .logger import Logger
from .stages import Stages

session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
)

###--------------------------------------------------------------------------------------------

def get_ssm_path(project, application, stage, key=None, prefix=None):
    return prefix + Contexts.encode_context_path(project, application, stage, key)

###--------------------------------------------------------------------------------------------

def load_ssm_path(parameters, path, parameter_type, prefix=None, decrypt=False):
    p = ssm.get_paginator('get_parameters_by_path')
    paginator = p.paginate(Path=path, Recursive=True, WithDecryption=decrypt, ParameterFilters=[{'Key': 'Type', 'Values': parameter_type}]).build_full_result()
    for parameter in paginator['Parameters']:
        key = parameter['Name'][len(path)+1:]
        if key in parameters:
            Logger.warn("Inherited parameter '{0}' overridden.".format(key))
        
        parameters[key] = {
                            'Value': parameter['Value'], 
                            'Path': parameter['Name'],
                            'Version': parameter['Version'],
                            'Date': parameter['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                        }
    return parameters

###--------------------------------------------------------------------------------------------

def load_context_ssm_parameters(project, application, stage, parameter_type, prefix=None, decrypt=False, uninherited=False):
    ### construct search path in hierachy with no key specified
    paths = Contexts.get_hierachy_context_paths(project, application, stage, key=None, prefix=prefix, allow_stages=(not stage is None), uninherited=uninherited)
    parameters = {}
    for path in paths:
        Logger.debug(f"Loading SSM parameters: path={path}")
        load_ssm_path(parameters, path, parameter_type, prefix, decrypt)
        for key, details in parameters.items():
            ### set Scope if it has not previousely been set, i.e. for newly loaded parameters
            if not 'Scope' in details.keys():
                details['Scope']= Contexts.translate_context(*Contexts.decode_context_path(details['Path'][len(prefix):])[0:3])
            ### set Stage if it has not previousely been set, i.e. for newly loaded parameters
            if not 'Stage' in details.keys():
                details['Stage'] = Stages.shorten('/'.join(Contexts.decode_context_path(details['Path'][len(prefix):])[2:3]))
            ### set Origin if it has not previousely been set, i.e. for newly loaded parameters
            if not 'Origin' in details.keys():
                details['Origin']= {
                    'Project': Contexts.decode_context_path(details['Path'][len(prefix):])[0],
                    'Application': Contexts.decode_context_path(details['Path'][len(prefix):])[1],
                    'Stage': Stages.shorten('/'.join(Contexts.decode_context_path(details['Path'][len(prefix):])[2:3])),
                }

    return parameters

###--------------------------------------------------------------------------------------------

def locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=None, uninherited=False):
    result = {}
    paths = list(reversed(Contexts.get_hierachy_context_paths(project, application, stage, key, prefix=prefix, allow_stages=(not stage is None), uninherited=uninherited)))
    for path in paths:
        Logger.debug(f"Describing SSM parameters: path={path}")
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
        if len(response['Parameters']) > 0:
            result = response['Parameters'][0]
            result['Scope'] = Contexts.translate_context(*Contexts.decode_context_path(result['Name'][len(prefix):])[0:3])
            result['Stage'] = Stages.shorten('/'.join(Contexts.decode_context_path(result['Name'][len(prefix):])[2:3]))
            result['Origin']= {
                'Project': Contexts.decode_context_path(result['Name'][len(prefix):])[0],
                'Application': Contexts.decode_context_path(result['Name'][len(prefix):])[1],
                'Stage': Stages.shorten('/'.join(Contexts.decode_context_path(result['Name'][len(prefix):])[2:3])),
            }

            break
    return result

###--------------------------------------------------------------------------------------------

def assert_ssm_parameter_no_namespace_overwrites(project, application, stage, key, prefix=None):
    """
        check if a parameter will overwrite parent or childern parameters (with the same namespaces) in the same stage (always uninherited)
        e.g.: 
            parameter a.b.c would overwrite a.b (super namespace)
            parameter a.b would overwrite a.b.c (sub namespace)
    """
    
    ### check children parameters
    path = prefix + Contexts.encode_context_path(project, application, stage, key)
    response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
    if len(response['Parameters']) > 0:
        raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other parameters in '{0}.*' namespace if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

    ### check parent parameters
    namespaces = key.split('.')
    for n in range(len(namespaces)-1):
        subKey = '.'.join(namespaces[0:n+1])
        path = get_ssm_path(project, application, stage, subKey, prefix)
        Logger.debug(f"Describing SSM parameters: path={path}")
        # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String']},{'Key':'Name', 'Values':[path]}])
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite parameter '{1}'.".format(key, subKey))

