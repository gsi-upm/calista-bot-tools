#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

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

# "I don't know' bot answer
unknown_answer = u"Lo siento, no te he entendido. Podrias reformularlo, ¿por favor?"
unknown_strict = u'Lo siento'

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
    
def check_response(response, concept, args):
    """
    Loads the json response and checks if it gets a valid response
    Returns a tuple, with wether the result is valid and the actual response
    (valid, response)
    """
    try:
        response_data = json.loads(response)
        dialog = response_data[u'dialog']
        
        # Dirty check. If the response is not "Hey, sorry. What were we talking about?"
        # we consider it valid. For the time being.
        #print "q: {query},\n response: {response}".format(query=response_data['dialog']['q'], response=response_data['dialog']['response'])
        
        if args.verbose > 3:
            print(u'Bot response: {response}'.format(response=dialog[u'response']))
        
        # We have a concept to check
        if concept:
            if u'topic' not in dialog:
                # Bad response
                return (False, dialog[u'response'])
            
            # We have a topic and a response:
            if concept in dialog[u'topic']:
                return (True, dialog[u'response'])
            
        unknown = unknown_strict if args.strict else unknown_answer
        
        if unknown in dialog[u'response']:
            return (False, dialog[u'response'])
        else:
            # I don't have a topic, but neither a "default" response, so
            # either a "Would you want to learn about this (TODO!)
            # or a generic identification answer
            return (True, dialog[u'response'])
        
    except Exception as e:
        # No json received. Invalid response.
        if args.verbose >3:
            print(u"Invalid response: "+ response, file=sys.stderr)
            print(e, file=sys.stderr)
    
    return (False, 'Invalid')

def main(args):
    
    if args.verbose > 1:
        print(u'Using agent: {agent}'.format(agent=args.agent))

    lines =  get_test_phrases(args.corpus)

    valid_responses = []
    invalid_responses = []

    # Ignore the header
    for line in lines[1:]:
        datos = line.split(",") 
        request = format_url(datos[0], args.url, args.agent)
        
        if args.verbose > 3:
            print(u'------------------------------------------------')
            print(u"Request URL: {url}".format(url=request))
        
        # Perform the request
        response = urllib.urlopen(request).read()
        
        if args.verbose > 3:
            print(u'Question: {question}'.format(question=datos[0]))
            if len(datos) > 1:
                print(u'Concept: {concept}'.format(concept=datos[1]))
        concept = None
        # Adds
        if len(datos) > 1:
            concept = datos[1]
            
        q_result = check_response(response, concept, args)
        if q_result[0]:
            valid_responses.append((datos[0],q_result[1]))
        else:
            invalid_responses.append((datos[0],q_result[1]))
    
    # Print wrong results with a lower verbosity level
    if args.verbose >2:
        print(u'------------------------------------------------------')
        print(u"Valid results:")
        for res in valid_responses:
            print(u"Q: {q}, R: {r}".format(q=res[0], r=res[1]))
        print(u'------------------------------------------------------')
    
    if args.verbose >1:
        print(u'------------------------------------------------------')
        print(u"Valid results:")
        for res in invalid_responses:
            print(u"Q: {q}, R: {r}".format(q=res[0], r=res[1]))
        print(u'------------------------------------------------------')
    
    # Always print final result
    print(u"Resultado: {valid} Validos, {invalid} No validos".format(valid=str(len(valid_responses)),
                                                                     invalid=str(len(invalid_responses))))
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tester for the calista-bot front-end, using a provided corpus", add_help=True)
    parser.add_argument('-u', '--url', default="http://localhost:8090", help="URL of the talkbot controller")
    parser.add_argument('-c', '--corpus', default="test_corpus.txt", help="CSV with the questions to test")
    parser.add_argument('-a', '--agent', default="TestAgent", help="User to use with the bot")
    parser.add_argument('-v', '--verbose', action='count', help="Print debug info")
    parser.add_argument('-s', '--strict', action='store_true', help="Consider non-gambit responses as valid.")
    parser.set_defaults(strict=False)
    args = parser.parse_args()
    main(args)
    