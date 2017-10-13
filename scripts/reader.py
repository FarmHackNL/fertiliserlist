#!/usr/bin/env python
import json
from io import BytesIO

import requests
import unicodecsv
import os


class Reader(object):
    def parse(self):
        raise NotImplementedError()


class GDOCReader(Reader):
    def __init__(self, hash, gid, fname=None):
        super(GDOCReader, self).__init__()
        self.hash = hash
        self.gid = gid
        self.columns = ['Name', 'From', 'To', 'Country',
                'Type', 'Unit', 'SpecificWeight', 'Volume',
                'N', 'Norg', 'Nmin', 'N-slow', 'N-ureum', 'NH4', 'NO3', 'N-Amide',
                'P2O5', 'K2O', 'MgO', 'CaO', 'SO3', 'Na2O', 'Cl', 'Cu', 'Co', 'B', 'Mo',
                'Fe', 'Mn', 'Zn', 'SiO2', 'Se', 'Pb']
        self.mapping = {}
        self.result = None
        self.fname = fname

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
