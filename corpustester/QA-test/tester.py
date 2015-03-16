#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import csv
import socket

import argparse

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
        print("Readed {lines} from the corpus {corpus}".format(lines=str(rcount), corpus=(args.corpus)), file=args.file)
    
    return data

def test_chatscript(question, args):
    '''
    Send the question to chatscript
    '''
    query = args.agent + '\0' + 'Duke\0' + question +'\0'
    
    s = socket.socket()
    s.connect((args.ip, args.port))
    s.send(query.encode('utf-8'))
    # Read response
    data = s.recv(1024)
    response = ""
    while data:
        response += data
        data = s.rcv(1024) 
    
    return response

def test_solr(question, args):
    '''
    send the question to solr
    '''
    
    return ""

def process_response(cs_responses, solr_responses, args):
    '''
    Process responses and print the results
    '''
    print "TODO"
    
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
    process_response(cs_responses, solr_responses, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tester for the calista-bot back-end, using a provided corpus", add_help=True)
    parser.add_argument('-i', '--ip', default="http://localhost:1234", help="Host for the Chatscript server")
    parser.add_argument('-p', '--port', default="1234", help="Port for the Chatscript server")
    parser.add_argument('-s', '--solr', defaults="http://localhost:8090/solr", help="Location of the Solr service")
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
    
