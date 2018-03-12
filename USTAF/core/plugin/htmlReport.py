#-------------------------------------------------------------------------------
# Name:        HTMLgenerator
# Purpose:
#
# Author:      yuboli
#
# Created:     20/07/2015
# Copyright:   (c) yuboli 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import shutil
import codecs
from jinja2 import Environment, FileSystemLoader
import sys, os


class HtmlGenerator(object):
    def __init__(self, data, path, template='report_template.html'):
        self.data = data
        self.template = template
        self.path = path + '/template'
        self.result_path = path + '/html'

    @property
    def _html_content(self):
        context = {"data" : self.data}
        TEMPLATE_ENVIRONMENT = Environment(loader=FileSystemLoader(self.path))
        return TEMPLATE_ENVIRONMENT.get_template(self.template).render(context)

    def generate(self, output_report_file):
        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)
        '''
        #copy static files to output path
        src_path = os.path.join(CURRENT_PATH, "templates", "static")
        dst_path = os.path.join(output_report_location, "static")
        if os.path.isdir(dst_path):
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)
        '''
        abs_output_report_file = os.path.join(self.result_path, output_report_file)
        with codecs.open(abs_output_report_file, 'w', encoding="utf_8") as f:
            f.write(self._html_content)
