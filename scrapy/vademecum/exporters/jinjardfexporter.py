# -*- coding: utf-8 -*-

import scrapy.contrib.exporter

from jinja2 import Environment, PackageLoader



class JinjaRDFExporter(scrapy.contrib.exporter.BaseItemExporter):
    ''' 
        Args:
            file(File) - a file
    '''
    
    def __init__(self, file, **kwargs):
        self.file = file
        self.env = Environment(loader=PackageLoader('vademecum.exporters', 'templates'))
        # Autoescape html
        self.env.autoescape = True
        # Create a list with all the items to export, each time a new
        # item is exported is added to this list, waiting to be write to
        # a file in finish_exporting
        self.items = []
        
        # The concepts are usually two or more words, separated by spaces
        # Replace them with a capitalized non-spaced version
        # i.e: palabra reservada --> PalabraReservada
        self.concepts = {}
        
    def export_item(self, item):
        ''' This method is called each time the scrapped_item signal is 
            received
            
            Args:
                item(Item):    The item scraped   
        '''
        
        # If the "broader" concept is the vademcum itself, point to the
        # concept instead, if exists, or nothing if not.
        #if item['broader'] == "http://www.dit.upm.es/~pepe/libros/vademecum/topics/3.html":
        
        # Replace the concept tag
        if 'concept' in item:
            if item['concept'] not in self.concepts:
                old_concept = item['concept']
            
                # First, make all first letters capitalize, them remove spaces
                concept_id = ''.join(item['concept'].title().split())
                self.concepts[item['concept']] = concept_id
        

        self.items.append(item)
    
    def finish_exporting(self):
        '''
        This method is called at the end of the exporting process, and
        its responsible of joining all the items in a single rdf file
        '''
        # Get namedIndividual template
        #named_individual = self.env.get_template("namedIndividual.rdf")
        # Get body template
        body = self.env.get_template("rdf_body.rdf")
        
        data = {}
        data['concepts'] = self.concepts
        data['items'] = self.items
        rdf_data = body.render(data=data)
        
        self.file.write(rdf_data.encode('utf8'))