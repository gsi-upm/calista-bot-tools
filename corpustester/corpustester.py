# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys, os
import codecs

root_folder = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(root_folder, 'QA-test')))

import tester

from flask import Flask

app = Flask(__name__)
app.debug = True

# TODO: Config file
corpus_file = "{root}/corpus/test_corpus.txt".format(root=root_folder)
cs_agent = "webtest"
cs_ip = "127.0.0.1:1024"
solr_url = "http://localhost:8080/solr/elearning"

# Keys for the response dicts
response_valid = 'valid'
response_invalid = 'invalid'
response_ne = 'ne'

@app.route('/')
def base():
    '''
    Index - Just a button to perform the test
    '''
    return open('{root}/static/templates/index.html'.format(root=root_folder), 'r').read()

@app.route('/test')
def test_corpus():
    '''
    Send the tests to the corpus and present the response.
    '''
    corpus = tester.read_corpus(corpus_file, (3, sys.stderr))
    
    cs_responses = []
    solr_responses = []
    # Perform the tests
    print(corpus, file=sys.stderr)
    for question in corpus:
        print(question, file=sys.stderr)
        # First, send the question to chatscript
        cs_responses.append(tester.test_chatscript(question[0], cs_agent, cs_ip))
        
        # Send to solr
        solr_responses.append(tester.test_solr(question[0], solr_url,
                                               (0, sys.stderr)))

    results = process_responses(corpus, cs_responses, solr_responses)
    
    return str(results)

def process_responses(corpus, cs_responses, solr_responses):
    '''
    Process the responses from CS and solr, and return structured data for the
    templates to display
    '''
    # valid, invalid, ne
    # ne = non-expected. This value indicates a response the 
    # systems is not supposed to respond. i.e., solr does not need
    # to respond chit-chat
    solr_results = {response_valid:0, response_invalid:0, response_ne:0}
    cs_results = {response_valid:0, response_invalid:0, response_ne:0}
    
    result = []
    
    for i in xrange(len(corpus)):
        cs_r = cs_responses[i]
        solr_r = solr_responses[i]
        line = corpus[i]
        
        current = {'question':line[0], 'concept':line[1]}
        
        # Do we have a solr response?
        if len(solr_r)!= 0:
            # Question, concept, solr_response
            s_r = process_solr(line[0], line[1], solr_r)
            solr_results[s_r[0]] += 1
            current['solr'] = s_r[1]
        else:
            # Bad response from solr
            solr_results[response_invalid] +=1
        
        # ChatScript
        cs_p = process_cs(line[0], line[1], line[2], cs_r)
        cs_results[cs_p]+=1
        current['cs'] = cs_r
        
        result.append(current)
    return {'counts':{'solr':solr_results, 'cs':cs_results}, 'r':result}


def process_solr(question, concept, solr_response):
    '''
    Process the solr response
    Returns a tuple, the first element being wether
    the result is valid, not valid, or unexpected
    the second the relevant elements in the response.
    '''
    if concept != '':
        # Solr should give a valid response
        solr_concept = solr_response[0]['title'].lower()
        # create the response data
        result = {}
        result['title'] = solr_response[0]['title']
        result['definition'] = solr_response[0]['definition']
        result['score'] = solr_response[0]['score']
        
        if concept in solr_concept:
            # Valid response
            return (response_valid, result)
        else:
            return (response_invalid, result)
            
    return (response_ne, {})
    
def process_cs(question, concept, expected, cs_response):
    '''
    Process the cs response
    '''
    if expected.strip() in cs_response:
        # Chat script has pick it
        return response_valid
    return response_invalid

if __name__ == '__main__':
    app.run()
