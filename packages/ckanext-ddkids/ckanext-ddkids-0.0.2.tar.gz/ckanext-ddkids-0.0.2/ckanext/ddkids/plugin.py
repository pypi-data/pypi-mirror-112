import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan.common import config
import re

from functools import wraps

def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        try:
            return memo[args]
        except KeyError:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper

@memoize
def all_vocab():
    try:
        return toolkit.get_action('vocabulary_list')()
    except toolkit.ObjectNotFound:
        return None

@memoize
def exclude_field(fieldname):
    return re.match(r'^.*?(_est|_se|_id)$', fieldname)

def fields_for_filter(resource):
    '''Returns sorted list of text and time fields of a datastore resource.'''

    if not resource.get('datastore_active', None):
        return []

    data = {
        'resource_id': resource['id'],
        'limit': 0
    }
    result = toolkit.get_action('datastore_search')({}, data)

    fields = map(lambda x: x['id'],
        filter(lambda x: not exclude_field(x['id']), result.get('fields', [])))

    return sorted(fields)

def filename_from_url(url):
    if(not url):
        return "";
    else:
        return url[url.rfind("/")+1:]

def sort_resources(resources):
    resources.sort(key=lambda x: filename_from_url(x["url"]))
    return resources

def clean_vocab_filter(f):
    parts = f.split(':')
    return '+' + parts[0].replace(' ', '_') + ':' + parts[1]

class DdkidsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, ):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'ddkids')

    def _modify_package_schema(self, schema):
        schema.update({
                'last_import': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'indicator_id': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'additional_notes': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'source_notes': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'year': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'update_frequency': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'use_cases': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'visualizations': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'contact_link': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')],
                'version_notes': [toolkit.get_validator('ignore_missing'),
                                toolkit.get_converter('convert_to_extras')]
            })
        for vocab in all_vocab():
            schema.update({
                vocab['name']: [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')(vocab['name'])]
                })

        # Update resource schema
        schema['resources'].update({
            'harvest_data_file_updated': [ toolkit.get_validator('ignore_missing')],
            'harvest_dictionary_file_updated': [ toolkit.get_validator('ignore_missing')],
            'harvest_metadata_file_updated': [ toolkit.get_validator('ignore_missing')]
            })

    def create_package_schema(self):
        schema = super(DdkidsPlugin, self).create_package_schema()
        self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(DdkidsPlugin, self).update_package_schema()
        self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(DdkidsPlugin, self).show_package_schema()
        schema.update({
                'last_import': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'indicator_id': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'additional_notes': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'source_notes': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'year': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'update_frequency': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'use_cases': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'visualizations': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'contact_link': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')],
                'version_notes': [toolkit.get_converter('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')]
            })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        for vocab in all_vocab():
            schema.update({
                vocab['name']: [toolkit.get_converter('convert_from_tags')(vocab['name']),
                    toolkit.get_validator('ignore_missing')]
                })

        schema['resources'].update({
            'harvest_data_file_updated': [ toolkit.get_validator('ignore_missing')],
            'harvest_dictionary_file_updated': [ toolkit.get_validator('ignore_missing')],
            'harvest_metadata_file_updated': [ toolkit.get_validator('ignore_missing')]
            })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def get_helpers(self):
        return {
                'all_vocab': all_vocab,
                'ddkids_drupal_url': config.get('ckan.ddkids.drupal.url'),
                'fields_for_filter': fields_for_filter,
                'sort_resources': sort_resources
                }

    def dataset_facets(self, facets_dict, package_type):
        del facets_dict['organization']
        del facets_dict['license_id']
        del facets_dict['groups']
        del facets_dict['tags']
        del facets_dict['res_format']

        vocabs = all_vocab()

        # Special Vocab sort
        # Topic, Subtopic, Scale, Available by Race and Ethnicity, Age Group, Nativity,
        # Gender, Geography, Time Scale, followed by all others alphabetically, followed by 'Format' last

        manual_order = [
            'Topic',
            'Subtopic',
            'Scale',
            'Available by Race and Ethnicity',
            'Age Group',
            'Nativity',
            'Gender',
            'Geography',
            'Time Scale'
        ]

        existing_vocab_names = map(lambda x: x['name'], vocabs)

        first_group = [value for value in manual_order if value in existing_vocab_names]
        second_group = sorted([value for value in existing_vocab_names if value not in manual_order])

        for vocab in (first_group + second_group):
            facets_dict['vocab_' + vocab.replace(' ', '_')] = toolkit._(vocab)

        # add these last
        facets_dict['tags'] = toolkit._('Tags')
        facets_dict['res_format'] = toolkit._('Formats')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict

    def before_map(self, m):
        m.redirect('/', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/organization', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/organization/{action}', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/group', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/group/{action}', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/tag', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/tag/{action}', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/revision', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/revision/{action}', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/user', '/dataset', _redirect_code="301 Moved Permanently")
        m.redirect('/user/register', '/dataset', _redirect_code="301 Moved Permanently")
        return m

    def after_map(self, m):
        return m

    def before_search(self, search_params):
        # Repace vocab fields that have spaces with a \
        vocab_filters = map(
          clean_vocab_filter,
          re.findall(r'vocab_.*?:".*?"', search_params['fq']))

        new_fq = re.sub(r'vocab_.*?:".*?"', '', search_params['fq']) + ' ' + ' '.join(vocab_filters)
        search_params['fq'] = new_fq
        return search_params

