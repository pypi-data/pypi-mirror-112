import os
import csv
import json

class Metadata:

    NAME = 'name'
    FIELD_TYPE = 'field_type'
    FIELD_VALUE = 'field_value'

    def __init__(self, state = None):
        self.fields = {}
        self.field_names = []
        if state:
            self.fields = state['fields']
            self.field_names = state['field_names']
            self.updated = state['updated']

    def add_field(self, name, type, value):
        self.field_names.append(name)

        self.fields[name] = {
            self.NAME: name,
            self.FIELD_TYPE: type,
            self.FIELD_VALUE: value
        }

    def read_field_value(self, name):
        return self.read_field_property(name, self.FIELD_VALUE)

    def get_field_names(self):
        return self.field_names

    def read_field_type(self, name):
        return self.read_field_property(name, self.FIELD_TYPE)

    def read_field_property(self, name, property_name):
        if name in self.fields:
            field = self.fields[name]
        else:
            field = None

        if field:
            return field[property_name]

    def get_state(self):
        # this class can't be serialized , method to pull state from this class
        # so it can be passed back in when this class is deserialized again
        return {
            "fields": self.fields,
            "field_names": self.field_names,
            "updated": self.updated
        }

class MetadataReader:

    TAG_FIELD_TYPE = 'tag'
    CSV_DELIM = ','
    TAG_DELIM = ';'

    def read(self, path):
        meta = Metadata()

        meta.updated = os.path.getmtime(path)

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.CSV_DELIM)
            line_number = 0
            for row in csv_reader:
                property_name = row[0]
                field_type = row[1]
                field_value = row[2]

                if line_number != 0:
                    read_value = self._read_property(property_name, field_type, field_value)
                    meta.add_field(property_name, field_type, read_value)

                line_number += 1

        return meta

    def _read_property(self, field_name, field_type, value):
        value_to_return = value
        is_tag_field = field_type == self.TAG_FIELD_TYPE

        if is_tag_field:
            if not value_to_return:
                value_to_return = []
            else:
                value_to_return = value_to_return.split(self.TAG_DELIM)

            # Tags is an internal field that needs to be formatted differently.
            if field_name == 'tags' or field_name == 'Tags':
                value_to_return = [{'name': tag} for tag in value_to_return]

        return value_to_return
