import scrapy
from vademecum.items import VademecumItem

class vademecumSpider(scrapy.Spider):
    
    # Test spider to get the vademecum.IO
    name = 'vademecum'
    allowed_domains = ['http://www.dit.upm.es/']
    
    start_urls = ['http://www.dit.upm.es/~pepe/libros/vademecum/topics/4.html']

    def parse(self, response):
        doc = VademecumItem()
        
        header = response.xpath('//p[@class="MsoHeader"]/ancestor::div/*[2]/descendant::*/*/text()').extract()
        header = ''.join(header).strip()
        # Replace wyrd spaces
        header = header.replace(u"\xa0", "")
        print header
        
        # The concept goes within parenthesis.
        if "(" in header:
            doc["concept"] = header[header.index("(")+1:-1]
            
        if header[0].isdigit():
            idn = ""
            i = 0
            while header[i].isdigit():
                idn += header[i]
                i +=1
            doc["identifier"] = idn
        
        if "identifier" in doc.keys():
            # The number is always followed by a dot.
            header = header.replace(doc["identifier"]+".", u"")
        if "concept" in doc.keys():
            header = header.replace("("+doc["concept"]+")", u"")
        doc["tittle"] = header.strip()
        return doc