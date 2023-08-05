import re
from .logger import Logger
from .config import Configs
from .providers import StoreProvider, Providers
from .stages import Stages
from .constants import *
from .exceptions import *

class SecretProvider(StoreProvider):
    def add(self, project, application, stage, key, value):
        raise NotImplementedError()
    def list(self, project, application, stage, uninherited, decrypt):
        raise NotImplementedError()
    def get(self, project, application, stage, key, revision=None):
        raise NotImplementedError()
    def delete(self, project, application, stage, key):
        raise NotImplementedError()
    def history(self, project, application, stage, key):
        raise NotImplementedError()

class SecretManager():

    def validate_key(self, key):
        Logger.info("Start validating secret key...")
        Logger.debug(f"Validating: key={key}")
        pattern = REGEX_PATTERNS['secret_key']
        if not re.match(pattern, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, pattern))
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))

    def list(self, stage, uninherited, decrypt):
        project = Configs.project
        application = Configs.application
        provider = Providers.SecretProvider()
        if uninherited:
            Logger.info(f"Start listing uninherited SSM secrets: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            Logger.info(f"Start listing SSM secrets: project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.list(project, application, stage, uninherited, decrypt)

    def add(self, stage, key, value):
        self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.SecretProvider()
        Logger.info(f"Start adding secrets: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
        return provider.add(project, application, stage, key, value)

    def get(self, stage, key, revision):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.SecretProvider()
        Logger.info(f"Start getting secret value: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
        return provider.get(project, application, stage, key, revision)

    def history(self, stage, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.SecretProvider()
        Logger.info(f"Start getting secret history: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
        return provider.history(project, application, stage, key)

    def delete(self, stage, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.SecretProvider()
        Logger.info(f"Start deleting secret: project={project}, application={application}, stage={Stages.shorten(stage)}, key={key}")
        return provider.delete(project, application, stage, key)

Secrets = SecretManager()
