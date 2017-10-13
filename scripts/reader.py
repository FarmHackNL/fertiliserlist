#!/usr/bin/env python
import json
from io import BytesIO

import requests
import unicodecsv
import os


class FertiliserReader(object):
    def __init__(self, fname=None):
        self.columns = [
            'Name', 'From', 'To', 'Country',
            'Type', 'Unit', 'SpecificWeight', 'Volume',
            'N', 'Norg', 'Nmin', 'N-slow', 'N-ureum', 'NH4', 'NO3', 'N-Amide',
            'P2O5', 'K2O', 'MgO', 'CaO', 'SO3', 'Na2O', 'Cl', 'Cu', 'Co', 'B', 'Mo',
            'Fe', 'Mn', 'Zn', 'SiO2', 'Se', 'Pb']
        self.mapping = {}
        self.result = None
        self.fname = fname

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
        return unicodecsv.DictReader(fd, delimiter=',', quotechar='"')

    def write(self, fname=None):
        fname = fname or self.fname
        assert fname, "Please provide filename"
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '{}.csv'.format(fname))
        with open(file_path, 'wb') as fd:
            w = unicodecsv.writer(fd, delimiter=',')
            w.writerow(self.columns)
            for e in self.result:
                w.writerow(e)


class SharedGDOCReader(GDOCReader):
    def __init__(self, **kwargs):
        super(SharedGDOCReader, self).__init__('1oplc6Zr62abCfWWfN68MPQUT8uVkaa6Mr8sDHl2LKNQ', '0', **kwargs)

    def parse(self):
        result = []
        for row in self.get_reader():
            e = {k: v for k, v in row.items() if k in self.columns}
            result.append(e)
        self.result = [[e.get(k, '').strip() for k in self.columns] for e in result]
        return self


if __name__ == "__main__":
    SharedGDOCReader(fname='fertilisers').parse().write()
