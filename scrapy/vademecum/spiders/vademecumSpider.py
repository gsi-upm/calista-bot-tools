# -*- coding: utf-8 -*-

import scrapy
from vademecum.items import VademecumItem

import re
import bs4
import json


class vademecumSpider(scrapy.Spider):
    
    # Test spider to get the vademecum.IO
    name = 'vademecum'
    allowed_domains = ['http://www.dit.upm.es/']        
    url_base = "http://www.dit.upm.es/~pepe/libros/vademecum/topics/{topic_uri}"
    
    start_urls = [url_base.format(topic_uri=str(i)+".html") for i in xrange(4, 385)]


    def parse(self, response):
        
        doc = VademecumItem()
        doc['url'] = response.url
        
        header = response.xpath('//p[@class="MsoHeader"]/ancestor::div/*[2]/descendant::*/*/text()').extract()
        header = ''.join(header).strip()
        # Replace wyrd spaces
        header = header.replace(u"\xa0", "")
        
        # We can proceed from here using regexp:
        # 1. abstract (palabra reservada)      ---  (\d+)\.\s(\S+)\s\((.*)\)
        # 4. Algoritmo [algorithm] (concepto)  ---  (\d+)\.\s(\S+)\s\[(.+)\]\s\((.+)\)
        # 20. Bytecode                         ---  (\d+)\.\s(\S+)
        # Métodos abstractos                   ---  (.*)
        #
        # There are some other cases:
        # 75. Fichero fuente [source code file]   ---  ^(\d+)\.\s+(.+)\[(.+)\]
        # número variable de argumentos (varargs)
        
        if "[" in header:
            # We are in the second case
            match = re.search("(\d+)\.\s(\S+)\s\[(.+)\]\s\((.+)\)", header)
            
            if match:
                # We should have 4 matches
                if match.lastindex == 4:
                    doc['title'] = match.group(2)
                    doc['alternative'] = match.group(3)
                    doc['concept'] = match.group(4)
            else:
                match = re.search("^(\d+)\.\s+(.+)\[(.+)\]$", header)
                if match:
                    doc['title'] = match.group(1)
                    doc['alternative'] = match.group(2)
        elif "(" in header:
            # The first case
            match = re.search("(\d+)\.\s(\S+)\s\((.*)\)", header)
            if match:
                # 3 matches
                if match.lastindex == 3:
                    doc['title'] = match.group(2)
                    doc['concept'] = match.group(3)
            else:
                match = re.search("^(.+)\s\((.*)\)$", header)
                
                if match:
                    doc['title'] = match.group(1)
                    doc['concept'] = match.group(2)
                
        elif header[0].isdigit():
            # The third case
            match = re.search("(\d+)\.\s*(\S+)", header)
            
            if match.lastindex == 2:
                doc['title'] = match.group(2)
        else:
            # just the title
            doc['title'] = header

        # Now we want the actual full-content, as well as the first sentence as a definition
        content = response.xpath('//p[@class="MsoNormal"]/*').extract()
        html_content = ' '.join(content)
        
        # Clear this content whit beautiful soup:
        body_soup = bs4.BeautifulSoup(html_content)
        
        # Give it a nice format
        body = ' '.join(body_soup.get_text().split()).replace(" ,", ",")
        
        if "." in body:
            # First sentence
            doc['description'] = body[:body.index('.')]
            
            #Full text
            doc['definition'] = body
        else:
            #Asume just one sentence
            doc['description'] = body
            doc['definition'] = body
            
        # Looks for links
        if "href" in html_content:
            links = response.xpath('//p[@class="MsoNormal"]/span/a/@href').extract()
            links = [self.url_base.format(topic_uri=link[:link.index("#")]) for link in links]
            try:
                pat = re.compile("href\=\"(\S+)#")
                match = re.findall("href\=\"(\S+)#", html_content)
                matched_links = [self.url_base.format(topic_uri=link) for link in match]
                
            except Exception as e:
                # Do nothing
                print e
            
            doc['links'] = links
            
                
        # I should chose either xpath or regexp...
        
        extables = response.xpath('//table[@class="MsoNormalTable"]/tr/td')
        examples = []
        
        for example in extables:
            table_content = example.xpath('p[contains(@class, "PreformattedText")]').extract()
            if table_content:
                examples.append(bs4.BeautifulSoup(' '.join(table_content)).get_text())
        
        doc['examples'] = examples
        # How do we add this?
        warning_note = response.xpath('//p[@align="center"]/b/span/text()').extract()
        
        topics = response.xpath('//p[@class="msoNormal"]/a/@href').extract()
        # get the "Related topics" links
        # The first one is the "parent" (broader) topic, 
        # the rest are "child" (narrower) topics.
        
        doc['broader'] = self.url_base.format(topic_uri=topics[0])
        doc['narrower'] = [self.url_base.format(topic_uri=topic) for topic in topics[1:]]
        
        return doc