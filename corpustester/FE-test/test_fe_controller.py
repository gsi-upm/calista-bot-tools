#!/usr/bin/python

import sys
import codecs
import string
import random
import argparse

from unidecode import unidecode

import urllib
import json

# Example request URL
#http://localhost:8090/gsibot/bottle/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user=UoUinQKS8YYlFAchLu9R&q=Hola&undefined=
#http://localhost:8090/gsibot/bottle/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user=UoUinQKS8YYlFAchLu9R&q=eres+el+profesor%3F&undefined=
url_format = u"{base}/TalkToBot?userAgent=web_html_v1&bot=Duke&type=json&user={user}&q={query}&undefined="

def get_test_phrases(corpus):
    """
    Read the corpus file, and returns a list with all the phrases
    """
    corpus = codecs.open(corpus, 'r', 'utf-8')
    lines = [line.replace(u"\n", u"") for line in corpus]
    return lines

def format_url(line, url, agent):
    
    # I am sure there is a nicer way for this, but...
    q = urllib.quote_plus(unidecode(line), "")
    
    request = url_format.format(base=url, user=agent, query=q)
    
    return request
    
def check_response(response, concept, verbose):
    """
    Loads the json response and checks if it gets a valid response
    """
    try:
        response_data = json.loads(response)
    
        # Dirty check. If the response is not "Hey, sorry. What were we talking about?"
        # we consider it valid. For the time being.
        #print "q: {query},\n response: {response}".format(query=response_data['dialog']['q'], response=response_data['dialog']['response'])
        
        if verbose:
            print(u'Bot response: {response}'.format(response_data['dialog']['response']))
        
        # We have a concept to check
        if concept:
            if u'topic' not in response_data['dialog']:
                # Bad response
                return False
            
            # We have a topic and a response:
            if concept in response_data['dialog'][u'topic']:
                return True

        if u"Lo siento," in response_data['dialog']['response']:
            return False
        else:
            # I don't have a topic, but neither a "default" response, so probably a
            # generic "i'm not the teacher" response.
            return True
        
    except Exception as e:
        # No json received. Invalid response.
        print u"Invalid response: "+ response
        if verbose:
            print e
    
    return False

def main(args):
    
    if args.verbose:
        print(u'Using agent: {agent}'.format(agent=args.agent))

    lines =  get_test_phrases(args.corpus)
    
    valid = 0
    notvalid = 0
    
    for line in lines:
        datos = line.split(",") 
        request = format_url(datos[0], args.url, args.agent)
        
        if args.verbose:
            print(u'------------------------------------------------')
            print(u"Request URL: {url}".format(url=request))
        
        # Perform the request
        response = urllib.urlopen(request).read()
        
        if args.verbose:
            print(u'Question: {question}'.format(question=datos[0]))
            if len(datos) > 1:
                print(u'Concept: {concept}'.format(concept=datos[1]))
        concept = None
        # Adds
        if len(datos) > 1:
            concept = datos[1]
        if check_response(response, concept, args.verbose):
            valid += 1
        else:
            notvalid += 1
            
    print u"Resultado: {valid} Validos, {invalid} No validos".format(valid=str(valid), invalid=str(notvalid))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tester for the calista-bot front-end, using a provided corpus", add_help=True)
    parser.add_argument('-u', '--url', default="http://localhost:8090", help="URL of the talkbot controller")
    parser.add_argument('-c', '--corpus', default="test_corpus.txt", help="CSV with the questions to test")
    parser.add_argument('-a', '--agent', default="TestAgent", help="User to use with the bot")
    parser.add_argument('-v', '--verbose', action='count', help="Print debug info")
    args = parser.parse_args()
    main(args)
    