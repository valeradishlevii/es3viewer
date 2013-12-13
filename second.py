# -*- coding: utf-8 -*-
import es3viewer
import sys

for filename in sys.argv[1:]:
    print filename
    pars = es3viewer.es3viewer(filename)
    pars.extraxt_metadata()
    for data in pars.get_metadata():
        print data['id']
        print data['value']
    pars.extract_zip_object()
    print "----"
    for data in pars.get_file_list():
        print data
