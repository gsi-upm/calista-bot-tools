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
    corpus = codecs.open('test_corpus.txt', 'r', 'utf-8')
    lines = [line.replace("\n", "") for line in corpus]
    return lines

def random_agent():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))
    
def format_url(line, url, agent):
    
    # I am sure there is a nicer way for this, but...
    q = urllib.quote_plus(unidecode(line), "")
    
    request = url_format.format(base=url, user=agent, query=q)
    
    return request
    
def check_response(response, concept):
    """
    Loads the json response and checks if it gets a valid response
    """
    try:
        response_data = json.loads(response)
    
        # Dirty check. If the response is not "Hey, sorry. What were we talking about?"
        # we consider it valid. For the time being.
        #print "q: {query},\n response: {response}".format(query=response_data['dialog']['q'], response=response_data['dialog']['response'])
        
        # We have a concept to check
        if concept:
            if u'topic' not in response_data['dialog']:
                # Bad response
                return False
            
            # We have a topic and a response:
            if concept in response_data['dialog'][u'topic']:
                return True

        if "Lo siento," in response_data['dialog']['response']:
            return False
        else:
            # I don't have a topic, but neither a "default" response, so probably a
            # generic "i'm not the teacher" response.
            return True
        
    except Exception as e:
        # No json received. Invalid response.
        print "Invalid response: "+ response
        print e
    
    return False

def main(url):

    agent = random_agent()
    lines =  get_test_phrases()
    
    valid = 0
    notvalid = 0
    
    for line in lines:
        datos = line.split(",") 
        request = format_url(datos[0], url, agent)
        
        # Perform the request
        response = urllib.urlopen(request).read()
        
        concept = None
        # Adds
        if len(datos) > 1:
            concept = datos[1]
        if check_response(response, concept):
            valid += 1
        else:
            notvalid += 1
            
    print "Resultado: {valid} Validos, {invalid} No validos".format(valid=str(valid), invalid=str(notvalid))

if __name__ == "__main__":

    url = "http://localhost:8090"
    if len(sys.argv) == 2:
        url = sys.argv[1]

    main(url)
