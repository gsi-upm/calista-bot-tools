# -*- coding: utf-8 -*-

import scrapy.contrib.exporter

import json


class jsonExporter(scrapy.contrib.exporter.BaseItemExporter):
    ''' 
        Args:
            file(File) - a file
    '''
    
    def __init__(self, file, **kwargs):
        self.file = file
        
        # Create a dict with all the items to export, each time a new
        # item is exported is added to this list, waiting to be write to
        # a file in finish_exporting
        self.items = {}
        
    def export_item(self, item):
        ''' This method is called each time the scrapped_item signal is 
            received
            
            Args:
                item(Item):    The item scraped   
        '''
        url = item.pop('resource')
        
        self.items[url] = {}
        for key, value in item.iteritems():
            if value != []:
                self.items[url][key] = value
    
    def finish_exporting(self):
        '''
        This method is called at the end of the exporting process, and
        its responsible of joining all the items in a single rdf file
        '''
        json.dump(self.items, self.file, indent=4)
    