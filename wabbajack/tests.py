"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os
import re
import base64
#import pprint
from django.test import TestCase
from django.db.models import get_apps

from django.conf import settings
from xml.etree.ElementTree import ElementTree
from urlparse import parse_qs

SCENARIES_DIR = 'scenaries'


class WabbajackTest(TestCase):
    """docstring for WabbajackTest"""

    fixtures = ['test_users.json', ]

    def do_test(self, uri, params, status=None):
        print uri, params, status
        from django.conf import settings
        if not uri.startswith(settings.STATIC_URL):
            resp = self.client.post(uri, data=params)
            self.assertTrue(resp.status_code in [status or 200, 302])

    def proceed_xml(self, filename):
        tree = ElementTree()
        tree.parse(filename)
        for request in tree.findall("request"):
            http = request.find("http")
            params = parse_qs(http.attrib.get('contents', ''))
            uri = http.attrib.get('url')
            self.do_test(uri, params)

    def proceed_wpp(self, filename):
        tree = ElementTree()
        tree.parse(filename)
        root = tree.find("Main")
        #pattern = re.compile(r"/HTTP\/1\.\d\s(\d+)/")
        for document in root.findall("Document"):
            uri = document.find("Request/URI").text
            params = dict()
            for param in document.find(
                    "Request/PostParameters").findall('Parameter'):
                name = param.find('Name').text
                value = param.find('Functions/Function/Value')
                if value.attrib.get('base64'):
                    value = base64.b64decode(value.text)
                else:
                    value = value.text
                params[name] = value
            status = int(re.match(r"HTTP\/1\.\d\s(\d+)",
                document.find("Request/HttpRequest/StatusLine").text).group(1))

            self.do_test(uri, dict(filter(lambda (k,v): v is not None, params.iteritems())), status)

    def test_all(self):
        """docstring for test_all"""
        scenaries_dir = getattr(settings, 'SCENARIES_DIR', SCENARIES_DIR)
        #assert self.client.login(username='admin', password='1')

        for app in get_apps():
            scenaries_path = os.path.join(os.path.dirname(
                os.path.abspath(app.__file__)), scenaries_dir)
            if os.path.isdir(scenaries_path):
                for files in os.listdir(scenaries_path):
                    if files.endswith(".wpp"):
                        self.proceed_wpp(os.path.join(scenaries_path, files))
                    if files.endswith(".xml"):
                        self.proceed_xml(os.path.join(scenaries_path, files))
