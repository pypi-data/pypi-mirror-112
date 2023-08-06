import os
import re
import logging
import csv
import ckan.plugins.toolkit as toolkit
import datetime

from import_finder import ImportFinder
from metadata_reader import MetadataReader, Metadata

from ckan.plugins.core import SingletonPlugin, implements
from ckanext.harvest.interfaces import IHarvester
from ckanext.harvest.model import HarvestObject, HarvestObjectError, HarvestGatherError
from ckan.lib.helpers import json
from ckan import model
from ckan.model import Session

log = logging.getLogger(__name__)

class DdkidsHarvester(SingletonPlugin):

    implements(IHarvester)

    def info(self):
        return {
            'name': 'ddkids',
            'title': 'DDKids Importer',
            'description': 'Harvests DDKids Metadata files',
            'form_config_interface': 'Text'
        }

    dataset_metadata_filename = 'dataset_metadata.csv'
    resource_metadata_filename = 'resource_metadata.csv'
    resource_dictionary_filename = 'dictionary.csv'
    harvester_name = 'ddkids'
    package_dict_meta = {
        'owner_org': 'brandeis'
    }

    CONTENT_PATH = 'path'
    CONTENT_RESOURCEPATHS = 'resourcepaths'
    CONTENT_METADATA = 'metadata'

    def gather_stage(self, harvest_job):
        try:
            self._set_config(harvest_job.source.config)

            object_ids = []
            import_dir = self.config['import_dir']

            log.debug("Searching data directory")

            import_finder = ImportFinder(harvest_job)
            import_directories = import_finder.find(import_dir, self.dataset_metadata_filename)

            for import_obj in import_directories:
                path = import_obj['path']

                metadata_path = self._get_metadata_path(path, self.dataset_metadata_filename)
                reader = MetadataReader()
                obj = reader.read(metadata_path)

                indicator_id = obj.read_field_value('indicator_id') or ''

                full_name = indicator_id + ' ' + obj.read_field_value('title')

                guid = re.sub(r'[^a-z0-9_-]', '-', full_name.lower())

                obj = HarvestObject(guid=guid[:100], job=harvest_job)

                resources = self._gather_resources_for_path(import_finder, path)

                if(resources == None):
                    return None

                obj.content = json.dumps({
                    self.CONTENT_PATH: path,
                    self.CONTENT_RESOURCEPATHS: resources
                })

                obj.save()
                object_ids.append(obj.id)

            return object_ids
        except Exception as e:
            msg = "Error gathering datasets for import - " + str(e)
            log.exception(msg)
            HarvestGatherError.create(msg, harvest_job)
            raise e

    def fetch_stage(self, harvest_object):
        self._set_config(harvest_object.job.source.config)

        obj = json.loads(harvest_object.content)
        object_path = obj.get(self.CONTENT_PATH)
        resourcepaths = obj.get(self.CONTENT_RESOURCEPATHS)

        metadata_path = self._get_metadata_path(object_path, self.dataset_metadata_filename)

        reader = MetadataReader()
        obj = reader.read(metadata_path)


        retobj = {
            self.CONTENT_PATH: object_path,
            self.CONTENT_METADATA: obj.get_state(),
            self.CONTENT_RESOURCEPATHS: resourcepaths
        }

        harvest_object.content = json.dumps(retobj)
        harvest_object.save()

        return True

    def import_stage(self, harvest_object):

        try:
            self._set_config(harvest_object.job.source.config)
            obj = json.loads(harvest_object.content)
            meta_state = obj[self.CONTENT_METADATA]
            meta = Metadata(meta_state)

            context = self._get_command_context()

            self._ensure_vocab_tags_exist(meta)

            dataset_crupdated = False

            log.debug("Importing Dataset: " + harvest_object.guid)

            indicator_id = meta.read_field_value('indicator_id')
            dataset_results = self._find_existing_package(indicator_id)

            if len(dataset_results) == 0:
                dataset_crupdated = True
                log.debug("Dataset new, creating: " + harvest_object.guid)
                package_dict = self._build_package(context, harvest_object, meta, {})
                dataset = toolkit.get_action('package_create')(context, package_dict)
            elif len(dataset_results) == 1:
                dataset = dataset_results[0]
                log.debug("Dataset found: " + harvest_object.guid)
                # Only update dataset if the metadata file is newer than the last import
                if (_time_is_newer(meta.updated, dataset.get('last_import', 0))):
                    log.debug("Dataset changed, updating: " + harvest_object.guid)
                    dataset_crupdated = True
                    package_dict = self._build_package(context, harvest_object, meta, dataset)
                    dataset = toolkit.get_action('package_update')(context, package_dict)
                else:
                    log.debug("Dataset unchanged, skipping: " + harvest_object.guid)
            else:
                log.error('Multiple datasets with the same indicator id were found!')
                return False

            resourcepaths = obj.get(self.CONTENT_RESOURCEPATHS)

            resources_crupdated = self._fetch_resources(dataset, resourcepaths)

            harvest_object.guid = dataset['id']
            harvest_object.package_id = dataset['id']
            harvest_object.current = True
            harvest_object.save()

            return True if resources_crupdated or dataset_crupdated else 'unchanged'

        except Exception as e:
            msg = "Error Importing Dataset - " + str(e)
            log.exception(msg)
            HarvestObjectError.create(msg, harvest_object, 'Import')
            return False

    def _get_command_context(self):
        return {'model': model, 'session': Session, 'user': self.config['user']}

    def _get_metadata_path(self, dir, name):
        path = os.path.join(dir, name)
        return path

    def _gather_resources_for_path(self, import_finder, path):
        resource_directories = import_finder.find_resources(
                path, 
                self.resource_metadata_filename, 
                self.resource_dictionary_filename, 
                self.config["data_file_extensions"])
        return resource_directories

    def _set_config(self, config_str):
        if config_str:
            self.config = json.loads(config_str)
        else:
            self.config = {}

    def _get_resource_file_name(self, path):
        return os.path.splitext(os.path.splitext(os.path.basename(path))[0])[0]

    def _upsert_resource(self, dataset, resource_config):
        cruptdated = False
        reader = MetadataReader()
        file_path = resource_config['file_path']
        meta_path = resource_config['meta_path']
        is_data_file = resource_config['is_data_file']
        dictionary_path = resource_config['dictionary_path']
        metadata = reader.read(meta_path)

        context = self._get_command_context()
        title = metadata.read_field_value('title')
        description = metadata.read_field_value('description') or ""
        prefix_len = len(self.config['import_dir'])
        file_path_len = len(file_path)
        file_name = os.path.basename(file_path)

        resource = self._find_existing_resource(dataset, file_name)

        file_modified = os.path.getmtime(file_path)
        metadata_modified = os.path.getmtime(meta_path)
        dictionary_modified = os.path.getmtime(dictionary_path) if is_data_file else ''

        new_resource = resource == None

        resource_path = self.config['file_url'] + file_path[prefix_len:file_path_len]

        # Handle creating or updating the resource item
        crupdated = False
        if(new_resource):
            log.debug("Creating Resource: " + file_name)
            crupdated = True

            # Configure the externally facing URL
            resource = toolkit.get_action('resource_create')(context, {
                'package_id': dataset['id'],
                'name': title,
                'description': description,
                'harvest_data_file_modified': str(file_modified),
                'harvest_dictionary_file_modified': str(dictionary_modified),
                'harvest_metadata_file_modified': str(metadata_modified),
                'url': resource_path
                })

        # Handle updating the data
        if(is_data_file and
                (new_resource or 
                     _time_is_newer(metadata_modified, resource.get('harvest_metadata_file_modified', 0)) or
                     _time_is_newer(file_modified, resource.get('harvest_data_file_modified', 0)) or
                     _time_is_newer(dictionary_modified, resource.get('harvest_dictionary_file_modified', 0)))):

            log.debug("Updating Resource Data and dictionary: " + file_name)
            crupdated = True

            # Read the dictionary
            data_dictionary = []
            
            for line in csv.DictReader(open(dictionary_path, 'rb')):
                data_dictionary.append(line)

            # Set up datastore
            data_fields = map(lambda row: ({
                'id': row['column'],
                'type': row['type'],
                'info': {
                    'notes': row['description'],
                    'type_override': row['type'],
                    'label': row['label']
                    },
                }), data_dictionary)

            if(resource['datastore_active']):
                toolkit.get_action('datastore_delete')(context, {
                    'resource_id': resource['id'],
                    'force': True
                })

            toolkit.get_action('datastore_create')(context, {
                'resource_id': resource['id'],
                'force': True,
                'fields': data_fields
            })

            # Configure resource views
            fields_to_show = map(lambda row: row['column'],
                    filter(lambda row: row['show'] == 'yes', data_dictionary))

            needs_new_view = new_resource

            if(not new_resource):
                log.debug("Updating resource view: " + file_name)
                tables_view = next(iter(filter(lambda v: v['view_type'] == 'datatables_view',
                    toolkit.get_action('resource_view_list')(context, { 'id': resource['id']}))), None)

                if(tables_view != None):
                    toolkit.get_action('resource_view_update')(context, {
                        'id': tables_view['id'],
                        'show_fields': fields_to_show
                        })
                else:
                    needs_new_view = True

            if(needs_new_view):
                log.debug("Creating new resource view : " + file_name)
                toolkit.get_action('resource_view_create')(context, {
                    'resource_id': resource['id'],
                    'view_type': 'datatables_view',
                    'title': 'Table',
                    'show_fields': fields_to_show
                    })

            toolkit.get_action('resource_update')(context, {
                'id': resource['id'],
                'name': title,
                'description': description,
                'harvest_data_file_modified': str(file_modified),
                'harvest_dictionary_file_modified': str(dictionary_modified),
                'harvest_metadata_file_modified': str(metadata_modified),
                'url': resource_path
                })

            # Trigger xloader
            log.debug("Triggering Xloader: " + file_name)
            toolkit.get_action('xloader_submit')(
                    context, {'resource_id': resource['id']})


        if(not crupdated):
            log.debug("Skipping Resource " + file_name)

        return crupdated

    def _find_resource_in_package(self, dataset, file_name):
        resource_meta = None
        if 'resources' in dataset and len(dataset['resources']):
            # Find resource in the existing packages resource list
            for res in dataset['resources']:
                # match the resource by its filename
                if os.path.basename(res.get('name')) != file_name:
                    continue
                # TODO: ignore deleted resources
                resource_meta = res
                # there should only be one file with the same name in each dataset, so we can break
                break
        return resource_meta

    def _fetch_resources(self, dataset, resources):
        return any(
                map(lambda r: self._upsert_resource(dataset, r),
                    resources))

    def _find_existing_package(self, indicator_id):
        data_dict = {'fq': '+indicator_id:%s' % indicator_id}
        package_show_context = self._get_command_context()
        search_response = toolkit.get_action('package_search')(
            package_show_context, data_dict)
        results = search_response['results']
        return results

    def _find_existing_resource(self, dataset, file_name):
        return next(iter(
            filter(lambda r: r['url'].split('/')[-1] == file_name, dataset['resources'])),
            None)

    def _add_harvester_metadata(self, package_dict, context):
        if self.package_dict_meta:
            # get organization dictionary based on the owner_org id
            if self.package_dict_meta.get('owner_org'):
                # get the organisation and add it to the package
                result = toolkit.check_access('organization_show', context)
                if result:
                    org_dict = toolkit.get_action('organization_show')(context, {'id': self.package_dict_meta['owner_org']})
                    if org_dict:
                        package_dict['organization'] = org_dict
                    else:
                        package_dict['owner_org'] = None
            # add each key/value from the meta data of the harvester
            for key,val in self.package_dict_meta.iteritems():
                package_dict[key] = val

        return package_dict

    def _get_tag_list(self, vocab):
        context = self._get_command_context()

        package_dict = {
            'id': vocab
        }

        try:
            response = toolkit.get_action('vocabulary_show')(context, package_dict)
        except toolkit.ObjectNotFound:
            response = None

        return map(lambda x: x['name'], response['tags']) if response != None else []

    def _create_vocab_tag(self, vocab, tag_name):
        context = self._get_command_context()

        package_dict = {
            'name': tag_name,
            'vocabulary_id': vocab
        }

        response = toolkit.get_action('tag_create')(context, package_dict)

    def _get_vocab_list(self):
        context = self._get_command_context()

        list = toolkit.get_action('vocabulary_list')(context, {})

        response = {}

        for vocab in list:
            name = vocab['name']
            id = vocab['id']

            response[name] = id

        return response

    def _create_vocab(self, vocab):
        context = self._get_command_context()

        package_dict = {
            'name': vocab
        }

        toolkit.get_action('vocabulary_create')(context, package_dict)

    def _is_vocab_field(self, field_name, field_type):
        # Tag fields are just passed in as strings so we don't classify
        # them as vocab fields
        is_vocab = field_type == 'string' \
                or (field_type == 'tag' and (field_name == 'Tags' or field_name == 'tags'))
        return is_vocab

    def _ensure_vocab_tags_exist(self, metadata):
        vocab_list = self._get_vocab_list()

        for key in metadata.get_field_names():
            field_value = metadata.read_field_value(key)
            field_type = metadata.read_field_type(key)

            if self._is_vocab_field(key, field_type):
                continue


            if key not in vocab_list:
                self._create_vocab(key)
                vocab_list = self._get_vocab_list()
                # We had to create the vocabulary, so automatically create the tags
                for tag in field_value:
                    self._create_vocab_tag(vocab_list[key], tag)
            else:
                tag_list = self._get_tag_list(vocab_list[key])
                for tag in field_value:
                    if not tag in tag_list:
                        self._create_vocab_tag(vocab_list[key], tag)

    def _convert_csv_field_to_ckan_field(self, key):
        return key.lower().replace(' ', '_')

    def _build_package(self, context, harvest_object, meta, package_dict):
        obj = json.loads(harvest_object.content)
        meta_state = obj['metadata']
        meta = Metadata(meta_state)

        package_dict['name'] = harvest_object.guid

        group_name = meta.read_field_value('group')

        package_dict = self._add_harvester_metadata(package_dict, context)

        for key in meta.get_field_names():
            field_value = meta.read_field_value(key)
            field_type = meta.read_field_type(key)

            if self._is_vocab_field(key, field_type):
                key = self._convert_csv_field_to_ckan_field(key)

            package_dict[key] = field_value

        package_dict['last_import'] = str(meta.updated)

        return package_dict


def _time_is_newer(a, b):
    if(not a):
        return False
    if(not b):
        return True

    return int(float(a)) > int(float(b))
