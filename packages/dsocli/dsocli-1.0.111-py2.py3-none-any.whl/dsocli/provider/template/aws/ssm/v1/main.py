import re
import boto3
from dsocli.exceptions import DSOException
from dsocli.logger import Logger
from dsocli.config import Configs
from dsocli.providers import Providers
from dsocli.templates import TemplateProvider
from dsocli.stages import Stages
from dsocli.constants import *
from dsocli.dict_utils import set_dict_value
from dsocli.contexts import Contexts
from dsocli.aws_utils import *


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

    def assert_no_scope_overwrites(self, project, application, stage, key):
        """
            check if a template will overwrite parent or childern parameters (with the same scopes) in the same stage (always uninherited)
            e.g.: 
                template a.b.c would overwrite a.b (super scope)
                template a.b would overwrite a.b.c (sub scope)
        """
        Logger.debug(f"Checking template overwrites: project={project}, application={application}, stage={stage}, key={key}")
        
        ### check children templates
        path = self.get_prefix(project, application, stage, key)
        # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String']},{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(response['Parameters']) > 0:
            raise DSOException("Template key '{0}' is not allowed in the given context becasue it would overwrite '{0}.{1}' and all other templates in '{0}.*' scope if any.".format(key,response['Parameters'][0]['Name'][len(path)+1:]))

        ### check parent templates
        scopes = key.split('.')
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_prefix(project, application, stage, subKey)
            Logger.debug(f"Describing templates: path={path}")
            # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String']},{'Key':'Name', 'Values':[path]}])
            response = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(response['Parameters']) > 0:
                raise DSOException("Template key '{0}' is not allowed in the given context becasue it would overwrite template '{1}'.".format(key, subKey))

###--------------------------------------------------------------------------------------------

    def list(self, project, application, stage, uninherited):
        ### construct search path in hierachy with no key specified
        paths = Contexts.get_hierachy_context_paths(project, application, stage, key=None, prefix=_settings['prefix'], allow_stages=True, uninherited=uninherited)
        # Logger.debug(f"SSM paths to search in order: {paths}")
        templates = {}
        for path in paths:
            Logger.debug(f"Loading SSM templates: path={path}")
            load_ssm_path(templates, path, ['StringList'], _settings['prefix'])

        result = {'Templates': []}
        for item in templates.items():
            result['Templates'].append({
                                    'Key': item[0], 
                                    # 'Contents': item[1]['Value'], 
                                    'Scope': item[1]['Scope'],
                                    'RevisionId': str(item[1]['Version']),
                                    'Date': item[1]['Date'],
                                    'Version': item[1]['Version'],
                                    'Path': item[1]['Path'],
                                    })

        return result

###--------------------------------------------------------------------------------------------

    def add(self, project, application, stage, key, contents):
        if len(contents) > 4096:
            raise DSOException(f"This template provider does not support templates larger than 4KB.")
        self.assert_no_scope_overwrites(project, application, stage, key)
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
                raise DSOException(f"Revision '{revision}' not found in the given context: project={project}, application={application}, stage={stage}, key={key}")
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
