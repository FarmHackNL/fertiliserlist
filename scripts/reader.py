#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import json
from io import BytesIO

import requests
import unicodecsv
import os


def normalize_name(name):
    if isinstance(name, basestring):
        return name.replace(u'®', u'')
    return name


def dict_reader_apply(reader, func):
    for row in reader:
        yield {k: func(v) for k, v in row.iteritems()}


class FertiliserReader(object):
    def __init__(self, fname=None):
        self.columns = [
            'Name', 'From', 'To', 'Country',
            'Type', 'Unit', 'SpecificWeight', 'Volume',
            'N', 'Norg', 'Nmin', 'N-slow', 'N-ureum', 'NH4', 'NO3', 'N-Amide',
            'P2O5', 'K2O', 'MgO', 'CaO', 'SO3', 'Na2O', 'Cl', 'Cu', 'Co', 'B', 'Mo',
            'Fe', 'Mn', 'Zn', 'SiO2', 'Se', 'Pb', 'CODE_NL_CL022']
        self.mapping = {}
        self.result = None
        self.fname = fname

    def get_data_path(self, fname):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '{}.csv'.format(fname))

    def parse(self):
        raise NotImplementedError()


class GDOCReader(FertiliserReader):
    def __init__(self, hash, gid, **kwargs):
        super(GDOCReader, self).__init__(**kwargs)
        self.hash = hash
        self.gid = gid

    def get_reader(self):
        url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid={}".format(self.hash, self.gid)
        fd = BytesIO(requests.get(url, verify=False).content)
        return dict_reader_apply(unicodecsv.DictReader(fd, delimiter=',', quotechar='"'), normalize_name)

    def write(self, fname=None):
        fname = fname or self.fname
        assert fname, "Please provide filename"
        file_path = self.get_data_path(fname)
        with open(file_path, 'wb') as fd:
            writer = unicodecsv.DictWriter(fd, fieldnames=self.columns, delimiter=',')
            writer.writeheader()
            for e in self.result:
                writer.writerow(e)

    def get_key(self, e):
        """
        define unique key / hash for a row which implies equality
        """
        return e['Name']

    def merge(self):
        """
        Merges the existing file (self.fname) with the new self.result
        """
        assert self.fname, "No existing file"
        assert self.result, "No parsed result {}".format(self.result)
        file_path = self.get_data_path(self.fname)
        with open(file_path, 'r') as fd:
            reader = unicodecsv.DictReader(fd, delimiter=',', quotechar='"')
            result = [e for e in reader]
            existing = {self.get_key(e): e for e in result}
            for row in self.result:
                key = self.get_key(row)
                if key not in existing:
                    result.append(row)
                    existing[key] = row
            self.result = result
        return self

    def parse(self):
        self.result = [{k: v for k, v in row.items() if k in self.columns} for row in self.get_reader()]
        return self


class SharedGDOCReader(GDOCReader):
    def __init__(self, **kwargs):
        super(SharedGDOCReader, self).__init__('1oplc6Zr62abCfWWfN68MPQUT8uVkaa6Mr8sDHl2LKNQ', '0', **kwargs)


if __name__ == "__main__":
    SharedGDOCReader(fname='fertilisers').parse().write()
