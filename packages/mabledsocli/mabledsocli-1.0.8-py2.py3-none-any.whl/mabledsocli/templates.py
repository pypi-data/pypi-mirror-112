
import os
import re
import jinja2
from jinja2 import meta
from .constants import *
from .config import Configs
from .providers import StoreProvider, Providers
from .parameters import Parameters
from .secrets import Secrets
from .logger import Logger
from .dict_utils import merge_dicts, deflatten_dict
from .exceptions import DSOException
from .stages import Stages

class TemplateProvider(StoreProvider):
    def list(self, project, application, uninherited):
        raise NotImplementedError()
    def add(self, project, application, key, contents):
        raise NotImplementedError()
    def delete(self, project, application, key):
        raise NotImplementedError()
    def get(self, project, application, key, revision=None):
        raise NotImplementedError()
    def history(self, project, application, key):
        raise NotImplementedError()


class TemplateManager():

    @property
    def default_render_path(self):
        return Configs.working_dir

    def validate_key(self, key):
        Logger.info("Start validating template key...")
        Logger.debug(f"Validating: key={key}")
        pattern = REGEX_PATTERNS['template_key']
        if not re.match(pattern, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, pattern))
        ### the regex does not check adjacent special chars
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))

        if '//' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '//'))

    def list(self, uninherited=False):
        project = Configs.project
        application = Configs.application
        provider = Providers.TemplateProvider()
        Logger.info(f"Start listing templates: project={project}, application={application}")
        renderPaths = Configs.get_template_render_paths()
        renderBasePath = Templates.default_render_path
        response = provider.list(project, application, uninherited)
        for template in response['Templates']:
            key = template['Key']
            if key in renderPaths:
                renderPath = renderPaths[key]
                # if not (renderPath == '.' or renderPath.startswith(f'.{os.sep}')):
                #     renderPath = os.path.join('./', renderPath)
            else:
                renderPath = f'.{os.sep}' + os.path.relpath(os.path.join(renderBasePath, key), Configs.working_dir) 

            template['RenderTo'] = renderPath
        
        return response

    def add(self, key, contents, render_path):
        self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.TemplateProvider()
        # if '..' in render_path:
        #     raise DSOException(MESSAGES['InvalidRenderPath'].format(render_path))
        # if render_path == '.' or render_path == f".{os.sep}":
        #     render_path = os.path.relpath(os.path.join(self.default_render_path, key), Configs.working_dir)
        # else:
        #     if '**' in render_path:
        #         render_path = render_path.replace('**', os.path.dirname(key))
        #     if '*' in render_path:
        #         render_path = render_path.replace('*', os.path.basename(key))
        # if not re.match('^[A-Za-z0-9._/$-]+$', render_path):
        #     raise DSOException(MESSAGES['InvalidRenderPath'].format(render_path))
        # if os.path.isdir(render_path):
        #     raise DSOException(MESSAGES['InvalidRenderPathExistingDir'].format(render_path))
        # if os.path.isabs(render_path):
        #     Logger.warn(f"Render path {render_path} is not releative to the application root.")
        # else:
        #     if not (render_path == '.' or render_path.startswith(f".{os.sep}")):
        #         render_path = os.path.join(f".{os.sep}", render_path)
        try:
            Logger.info(f"Start adding template: project={project}, application={application}, key={key}, render_path={render_path}")
            result = provider.add(project, application, key, contents)
            result['RenderTo'] = render_path
        finally:
            if os.path.abspath(render_path) == os.path.abspath(os.path.join(self.default_render_path, key)):
                Configs.unregister_template_custom_render_path(key)
            else:
                Configs.register_template_custom_render_path(key, render_path)
        return result

    def get(self, key, revision=None):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.TemplateProvider()
        Logger.info(f"Start getting template contents: project={project}, application={application}, key={key}")
        return provider.get(project, application, key, revision)

    def history(self, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.TemplateProvider()
        Logger.info(f"Start getting template history: project={project}, application={application}, key={key}")
        return provider.history(project, application, key)

    def delete(self, key):
        # self.validate_key(key)
        project = Configs.project
        application = Configs.application
        provider = Providers.TemplateProvider()
        Logger.info(f"Start deleting template: project={project}, application={application}, key={key}")
        try:
            result = provider.delete(project, application, key)
        finally:
            Configs.unregister_template_custom_render_path(key)
        return result

    def render(self, stage, limit=''):
        project = Configs.project
        application = Configs.application
        Logger.info(f"Start rendering templates: project={project}, application={application}, stage={Stages.shorten(stage)}")

        if Stages.is_default(stage):
            Logger.warn("No stage has been provided for rendering templates, using 'default'.")

        Logger.info("Loading parameters...")
        parameters = Parameters.list(stage, uninherited=False)

        merged = deflatten_dict({x['Key']: x['Value'] for x in parameters['Parameters']})

        Logger.info("Loading secrets...")
        secrets = Secrets.list(stage, uninherited=False, decrypt=True)

        Logger.info("Merging parameters...")
        merge_dicts(deflatten_dict({x['Key']: x['Value'] for x in secrets['Secrets']}), merged)

        Logger.info("Loading templates...")
        templates = self.list()['Templates']

        jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)

        Logger.info("Rendering templates...")
        rendered = []
        for item in templates:
            key = item['Key']
            if not key.startswith(limit): continue

            renderPath = item['RenderTo']
            if os.path.isdir(renderPath):
                raise DSOException("There is an existing directory at the template render path '{renderPath}'.")
            if os.path.dirname(renderPath):
                os.makedirs(os.path.dirname(renderPath), exist_ok=True)

            Logger.debug(f"Rendering template: key={key}")
            try:
                template = jinja_env.from_string(self.get(key)['Contents'])
            except:
                Logger.error(f"Failed to load template: {key}")
                raise
            # undeclaredParams = jinja2.meta.find_undeclared_variables(env.parse(template))
            # if len(undeclaredParams) > 0:
            #     Logger.warn(f"Undecalared parameter(s) found:\n{set(undeclaredParams)}")
            try:
                renderedContent = template.render(merged)
            except Exception as e:
                Logger.error(f"Failed to render template: {key}")
                msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
                raise DSOException(msg)

            with open(renderPath, 'w', encoding='utf-8') as f:
                f.write(renderedContent)
            
            rendered.append({'Key':key, 'RenderTo': renderPath})

        return rendered


Templates = TemplateManager()