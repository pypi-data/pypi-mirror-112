
import re
from .constants import *
from .exceptions import DSOException
from .config import Configs
from .stages import Stages

class ContextUtils():

    contexts_translation_matrix = {
        'default': {
            'default': {
                'default': {
                    '0': "Global",
                },
                'stage': {
                    '0': "Global Stage",
                    'n': "Global Stage Numbered",
                },
            },
        },
        'project': {
            'default': {
                'default': {
                    '0': "Project",
                },
                'stage': {
                    '0': "Project Stage",
                    'n': "Project Stage Numbered",
                },
            },
            'application': {
                'default': {
                    '0': "Application",
                },
                'stage': {
                    '0': "Application Stage",
                    'n': "Application Stage Numbered",
                },
            },
        },
    }

    def translate_context(self, project, application, stage):
        project_idx = 'default' if Configs.project == 'default' else 'project'
        application_idx = 'default' if Configs.application =='default' else 'application'
        stage_idx = 'default' if Stages.is_default(stage) else 'stage'
        n_idx = '0' if Stages.is_stage_default_env(stage) else 'n'
        return self.contexts_translation_matrix[project_idx][application_idx][stage_idx][n_idx]

    def encode_context_path(self, project, application, stage):
        result = f"/{project}"
        ### every application must belong to a project, no application overrides allowed in the default project
        if not project == 'default':
            result += f"/{application}"
        else:
            result += "/default"
        stage = Stages.normalize(stage)
        result += f"/{stage}"
        return result

    def decode_context_path(self, path):
        """
            path is in the form of [/]project/application/stage/env_no
        """
        parts = path.split('/')
        if not parts[0]: parts.pop(0)
        project = parts[0]
        application = parts[1]
        stage = f"{parts[2]}/{parts[3]}"
        return project, application, stage


Contexts = ContextUtils()