#!/usr/bin/python

import sys
import codecs
import string
import random

from unidecode import unidecode

import urllib
import json

# Example request URL
#http://localhost:8090/gsibot/bottle/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user=UoUinQKS8YYlFAchLu9R&q=Hola&undefined=
#http://localhost:8090/gsibot/bottle/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user=UoUinQKS8YYlFAchLu9R&q=eres+el+profesor%3F&undefined=
url_format = "{base}/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user={user}&q={query}&undefined="

def get_test_phrases():
    """
    Read the corpus file, and returns a list with all the phrases
    """
    corpus = codecs.open('qlist.txt', 'r', 'utf-8')
    lines = [line.replace("\n", "") for line in corpus]
    return lines

def random_agent():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))
    
def format_url(line, url, agent):
    
    # I am sure there is a nicer way for this, but...
    q = urllib.quote_plus(unidecode(line), "")
    
    request = url_format.format(base=url, user=agent, query=q)
    
    return request
    
def get_response_data(response):
    """
    Loads the json response and returns parts of it.
    """
    response_data = json.loads(response)
    # TODO: Add concept
    return {"question": response_data['dialog']['q'], "botanswer": response_data['dialog']['response']}
        
def main(url):

    agent = random_agent()
    lines =  get_test_phrases()
    
    responses = []
    
    # Get 10 random lines, instead of the full list
    
    
    #rlines = [lines.pop(random.randrange(len(lines))) for _ in xrange(10)]
    for line in lines:
        datos = line.split(",") 
        request = format_url(datos[0], url, agent)
        
        # Perform the request
        response = urllib.urlopen(request).read()
        
        # Adds
        responses.append(get_response_data(response))
    
    # Select 10 responses that are not "Lo siento, no he entendido la pregunta"
    errorline = "Lo siento"
    rlines = []

    while len(rlines) <10:
        ri = random.randrange(len(responses))
        botanswer = responses[ri]['botanswer'] 
        if len(botanswer) != 0:
            if  not botanswer.startswith(errorline):
                rlines.append(responses.pop(ri))
     
    
    # Add the last task for the live question
    rlines.append({'question': '', 'botanswer': '', 'boturi': url})
    
    print json.dumps(rlines, indent=4)

if __name__ == "__main__":

    url = "http://localhost:8090"
    if len(sys.argv) == 2:
        url = sys.argv[1]

    main(url)
