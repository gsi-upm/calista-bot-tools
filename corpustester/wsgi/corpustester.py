# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys, os

root_folder = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(root_folder, '../QA-test')))

import tester

from flask import Flask

app = Flask(__name__)

# TODO: Config file
corpus_file = "../corpus/test_corpus.txt"
cs_agent = "webtest"
cs_ip = "127.0.0.1:1024"
solr_url = "http://localhost:8080/solr/elearning"
@app.route('/')
def base():
    '''
    Index - Just a button to perform the test
    '''
    return open('{root}static/templates/index.html'.format(root=root_folder), 'r').read()

@app.route('/test')
def test_corpus():
    '''
    Send the tests to the corpus and present the response.
    '''
    corpus = tester.read_corpus(corpus_file, (0, sys.stderr))
    
    cs_responses = []
    solr_responses = []
    # Perform the tests

    for question in corpus:
        # First, send the question to chatscript
        cs_responses.append(tester.test_chatscript(question[0], cs_agent, cs_ip))
        
        # Send to solr
        solr_responses.append(tester.test_solr(question[0], solr_url,
                                               (0, sys.stderr)))
    
    
    return str(cs_responses + solr_responses)

if __name__ == '__main__':
    app.debug = True
    app.run()