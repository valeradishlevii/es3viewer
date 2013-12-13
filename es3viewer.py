# -*- coding: utf-8 -*-
from base64 import b64decode
from lxml import etree
import zipfile
import random


class es3viewer:
    def __init__(self, filename):
        self.filename = filename
        self.metadata = []
        self.zip = []
        self.mimes = []
        self.root = etree.XML(open(self.filename, 'rb').read())
        #self.ns = {'es': 'https://www.microsec.hu/ds/e-szigno30#',
        #         'ds': 'http://www.w3.org/2000/09/xmldsig#'}
        self.ns = dict(map(lambda x: [x, self.root.nsmap[x]], filter(None, self.root.nsmap)))

    def xpath(self, expr):
        return self.root.xpath(expr, namespaces=self.ns)

    def extraxt_metadata(self):
        self.metadata.append({'id': 'Title',
            'value': self.xpath("//es:DossierProfile/es:Title")[0].text})
        self.metadata.append({'id': 'E-category',
            'value':
            self.xpath("//es:DossierProfile/es:E-category")[0].text})
        self.metadata.append({'id': 'CreationDate',
            'value':
            self.xpath("//es:DossierProfile/es:CreationDate")[0].text})

    def extract_zip_object(self):
        r = self.xpath('//es:Document/es:DocumentProfile/es:BaseTransform/es:Transform[@Algorithm="zip"]/../../../ds:Object')
        mime = self.xpath('//es:Document/es:DocumentProfile/es:BaseTransform/es:Transform[@Algorithm="zip"]/../../es:Format/es:MIME-Type')
        for mtype in mime:
            if len(mtype.attrib['extension']) > 0:
                self.mimes.append(mtype.attrib['extension'])
            else:
                self.mimes.append(mtype.attrib['subtype'])
        for Doc in r:
            prefix = random.choice('abcdefghij123456879')
            zipfilename = "arch" + Doc.attrib['Id'] + prefix + ".zip"
            open(zipfilename, 'wb').write(b64decode(Doc.text))
            f = file(zipfilename)
            self.zip.append(zipfile.ZipFile(f))

    def get_file_list(self):
        i = 0
        for zip in self.zip:
            for f in sorted(zip.namelist()):
                open(f + '.' + self.mimes[i], 'wb').write(zip.read(f))
                i += 1
                yield f

    def get_metadata(self):
        for f in sorted(self.metadata):
            yield f
