import re
from .logger import Logger
from .config import Configs
from .providers import StoreProvider, Providers
from .stages import Stages
from .constants import *
from .exceptions import *


class ParameterProvider(StoreProvider):
    def add(self, project, application, stage, key, value):
        raise NotImplementedError()
    def list(self, project, application, stage, uninherited):
        raise NotImplementedError()
    def get(self, project, application, stage, key, revision=None):
        raise NotImplementedError()
    def delete(self, project, application, stage, key):
        raise NotImplementedError()
    def history(self, project, application, stage, key):
        raise NotImplementedError()


class ParameterManager():

    def validate_key(self, key):
        Logger.info("Start validating parameter key...")
        Logger.debug(f"Validating: key={key}")
        pattern = REGEX_PATTERNS['parameter_key']
        if not re.match(pattern, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, pattern))
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))
            
    def list(self, stage, uninherited=False, filter=None):
        project = Configs.project
        application = Configs.application
        provider = Providers.ParameterProvider()
        Logger.info(f"Start listing SSM parameters: project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.list(project, application, stage, uninherited, filter)

    def add(self, stage, key, value):
        self.validate_key(key)
        project = Configs.project
        application = Configs.application
        Logger.info(f"Start adding parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        provider = Providers.ParameterProvider()
        return provider.add(project, application, stage, key, value)

    def get(self, stage, key, revision):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.ParameterProvider()
        Logger.info(f"Start getting the value of parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.get(project, application, stage, key, revision)

    def history(self, stage, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.ParameterProvider()
        Logger.info(f"Start getting the history of parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.history(project, application, stage, key)

    def delete(self, stage, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.ParameterProvider()
        Logger.info(f"Start deleting parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.delete(project, application, stage, key)

Parameters = ParameterManager()