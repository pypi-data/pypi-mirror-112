from ckanext.harvest.model import HarvestGatherError
import os
from ckanext.ddkids.harvesters.metadata_reader import MetadataReader, Metadata

class ImportFinder:

    def __init__(self, harvest_job):
        self.harvest_job = harvest_job

    def find(self, import_dir, metadata_filename):
        paths = []
        found_paths = []

        for dirName, subdirList, fileList in os.walk(import_dir):
            if self._has_file(dirName, metadata_filename) != None:
                paths.append({ 'path': dirName })

        return paths

    def find_resources(self, directory, metadata_filename, dictionary_filename, data_file_extensions):
        paths = []
        reader = MetadataReader()

        for o in os.listdir(directory):
            path = os.path.join(directory, o)

            if os.path.isdir(path):
                meta_path = self._has_file(path, metadata_filename)
                dictionary_path = self._has_file(path, dictionary_filename)
                obj = reader.read(meta_path)
                fileName = obj.read_field_value('file')

                is_data_file = self._is_data_file(data_file_extensions, fileName)

                if(meta_path == None):
                    HarvestGatherError.create("Metadata path does not exist for resource: " + path, self.harvest_job)
                    return None

                if(is_data_file and dictionary_path == None):
                    HarvestGatherError.create("Dictionary path does not exist for resource: " + path, self.harvest_job)
                    return None

                for file in os.listdir(path):
                    is_excluded = file != fileName

                    if not is_excluded:
                        file_path = os.path.join(path, file)
                        paths.append({ 
                            'path': file, 
                            'meta_path': meta_path, 
                            'dictionary_path': dictionary_path, 
                            'file_path': file_path,
                            'is_data_file': is_data_file 
                            })

        return paths

    def _is_data_file(self, data_file_extensions, file_name):
        return any(
                map(lambda ex: file_name.endswith('.' + ex),
                    data_file_extensions))

    def _get_path(self, dir, filename):
        path = os.path.join(dir, filename)
        return path

    def _has_file(self, dir, filename):
        path = self._get_path(dir, filename)
        exists = os.path.isfile(path)

        if exists:
            return path
