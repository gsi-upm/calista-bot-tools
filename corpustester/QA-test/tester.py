#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import csv
import socket
import requests

from unidecode import unidecode

import argparse

solr_base = "{url}/select"

cs_gambit = ""
cs_error = "Lo siento, no te he entendido. Podrias reformularlo, ¿por favor?"

def read_corpus(args):
    '''
    Read and return the corpus data from a CSV
    '''
    
    f_csv = open(args.corpus, 'r')
    
    reader = csv.reader(f_csv)
    data = []
    rcount = 0
    for row in reader:
        if rcount != 1:
            # Not the header
            data.append(row)
        rcount+=1
        
    if args.verbose >2:
        print("Readed {lines} from the corpus {corpus}".format(lines=str(rcount), corpus=(args.corpus)), file=args.output)
    
    return data

def test_chatscript(question, args):
    '''
    Send the question to chatscript
    '''
    query = args.agent + '\0' + 'Duke\0' + question +'\0'
    
    s = socket.socket()
    # Split host and port
    cs_tcp = args.ip.split(":")
    s.connect((cs_tcp[0],int(cs_tcp[1])))
    s.send(query)
    # Read response
    data = s.recv(1024)
    response = ""
    while data:
        response += data
        data = s.recv(1024) 
    
    return response

def test_solr(question, args):
    '''
    Send the question to solr
    '''
    url = solr_base.format(url=args.solr)
    words = question.split(" ")
    # We use solr's dismax for full phrase search
    # The values should probably be a config option
    
    payload= {'q':question, 'wt':'json', 'rows':'1',
              'defType':'dismax', 'qf':'title^10.0 description^2.0'}
    
    if args.verbose >2:
        print("Sending {q} to solr".format(q=str(question)),file=args.output)
    response = requests.get(url, params=payload).json()
    
    return response['response']['docs']
    
def process_response(cs_responses, solr_responses, corpus, args):
    '''
    Process responses and print the results
    '''
    solr_valid = 0
    solr_invalid = 0
    cs_valid = 0
    cs_invalid = 0
    
    for i in xrange(len(cs_responses)):
        cs_r = cs_responses[i]
        solr_r = solr_responses[i]
        line = corpus[i]
        
        if args.verbose >2:
            print("-----------------------------------------------", file=args.output)
            print("CSV Line: {line}".format(line=line), file=args.output)
            print("Question: {q}".format(q=line[0]), file=args.output)
        
        # Do we have a concept?
        if line[1] != '':
            concept = line[1]
            
            # Solr should now about this
            if len(solr_r) != 0:
                solr_concept = unidecode(solr_r[0]['title']).lower()
                if unidecode(concept).strip() in solr_concept:
                    if args.verbose >2:
                        print(u"Valid Solr Concept: {solr_r}".format(solr_r=solr_concept), file=args.output)
                    solr_valid += 1
                else:
                    if args.verbose > 2:
                        print(u"Invalid Solr Concept: {concept}, Expected: {ex}".format(concept=solr_concept, ex=concept), file=args.output)
                    solr_invalid += 1
            else:
                if args.verbose >2:
                    print(u"Solr Concept: None", file=args.output)
                solr_invalid +=1
                    
                
        # CS should respond either with the sentence, or sending info to maia
        if line[2] in cs_r:
            if args.verbose >2:
               print(u"Valid CS Response: {cs_r}".format(cs_r=unidecode(cs_r)), file=args.output)
            cs_valid +=1
        else:
            if args.verbose >2:
                print("Invalid CS Response: {cs_r}".format(cs_r=cs_r), file=args.output)
            cs_invalid +=1
            
        if args.verbose >2:
            print("-----------------------------------------------", file=args.output)
            
    cs_percent = 100 *cs_valid / (cs_valid+cs_invalid)
    solr_percent = 100 *solr_valid / (solr_valid+solr_invalid)
    print("Total CS questions: {total}".format(total=str(cs_valid+cs_invalid)), file=args.output)
    print("Valid CS responses: {valid} ({percentage} %)".format(valid=str(cs_valid),
                                                                percentage=str(cs_percent)),
                                                                file=args.output)
    print("Total SOLR questions: {total}".format(total=str(solr_valid+solr_invalid)), file=args.output)
    print("Valid SOLR responses: {valid} ({percentage} %)".format(valid=str(solr_valid),
                                                                  percentage=str(solr_percent)),
                                                                  file=args.output)
    
def main(args):
    '''
    Performs the tests
    '''
    
    # Reads the questions from the corpus
    csv_lines = read_corpus(args)
    
    cs_responses = []
    solr_responses = []
    for question in csv_lines:
        # First, send the question to chatscript
        cs_responses.append(test_chatscript(question[0], args))
        
        # Send to solr
        solr_responses.append(test_solr(question[0], args))
        
    # Check the responses and print the results
    process_response(cs_responses, solr_responses, csv_lines, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tester for the calista-bot back-end, using a provided corpus", add_help=True)
    parser.add_argument('-i', '--ip', default="127.0.0.1:1024", help="Host for the Chatscript server")
    parser.add_argument('-s', '--solr', default="http://localhost:8080/solr/elearning", help="Location of the Solr service")
    parser.add_argument('-c', '--corpus', default="test_corpus.txt", help="CSV with the questions to test")
    parser.add_argument('-a', '--agent', default="TestAgent", help="User to use with the bot")
    parser.add_argument('-v', '--verbose', action='count', help="Print debug info")
    parser.add_argument('-p', '--permisive', action='store_true', help="Consider gambit responses as valid.")
    parser.add_argument('-o', '--output', default=sys.stdout, help="Output file")
    parser.set_defaults(permisive=False)
    args = parser.parse_args()
    # Get log output
    if args.output != sys.stdout:
        args.output = codecs.open(args.output, 'w+', 'utf-8-sig')
    main(args)
    
