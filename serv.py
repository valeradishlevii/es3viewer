# -*- coding: utf-8 -*-
import web
#import re
import es3viewer
#import model
import json

urls = ('/upload', 'Upload',
        '/get/(\d*)/', 'GetImage',
        '/isready/(\d*)/', 'IsImageReady')


class GetImage:
    def GET(self, id):
        return 'GetImage'


class IsImageReady:
    def GET(self, id):
        return 'IsImageReady'


class Upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="file" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        mydoc = web.input(file={})['file']
        f = open('/tmp/es3viewer/' + mydoc.filename, 'wb')
        f.write(mydoc.value)
        #n = model.new_task(mydoc.filename, 0, '/tmp/converterdir/' + mydoc.filename)
        pars = es3viewer.es3viewer('/tmp/converterdir/' + mydoc.filename)
        pars.extraxt_metadata()
        return  json.dumps([dict([['id', x['id']], ['value', x['value']]]) for x in pars.get_metadata()])

web.config.debug = False
app = web.application(urls, globals())
app.run()
