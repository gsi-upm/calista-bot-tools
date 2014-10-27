#!/usr/bin/python

import sys
import argparse

import re

# The command line options:
# The arguments I can take:
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plotable", help="Print the data in a plotable format",
                    action="store_true")
parser.add_argument("-n", "--noerrors", help="Do not include the errors",
                    action="store_true")
    
# The log input/oputput
parser.add_argument("-l", "--logfile", type=str, help="The file with the logs",
                    required=True)
parser.add_argument("-o", "--outfile", help="If specified, write the result to the file",)

# List of modules, by the name it can be identified in the log
modules = ['Unitex', 'ChatScript', 'SIREN', 'JASON']

# Input "flag"
# The line that identifies the first line of a new question-answer block
inputLine = "Unitex input: "

# The answer when the bot doesn't know how to respond.
badResponse = "Hey, sorry. What were we talking about?"


def modules_in_block(logtext):
    """
    Find what modules intervene in a given question-answer block
    """
    mods = []
    #Search for each module
    for mod in modules:
        if mod in logtext:
            mods.append(mod)
    return mods

def break_logs(logdata):
    """
    Given the full log, break it by user and questions
    """
    
    # Search for the different users first
    # Asume the user will appear in the inputLine
    user_regex = re.compile("\[user:\s(.+)\]\s"+inputLine.replace(" ", "\s"))
    
    # As usual, probably not the best way, specially with HUGE logs.
    # Maybe it will work better using a bash script, and providing
    # the identified users to this one.
    users = []
    for u in user_regex.finditer(logdata):
        if u.group(1) not in users:
            users.append(u.group(1))
    # break into lines
    ldata = logdata.split("\n")
    
    logs_by_users = {}
    
    for user in users:
        # Get the lines for this user
        user_data = [line for line in ldata if user in line]
        
        # input start lines
        start_lines = [idx for idx, line in enumerate(user_data) if inputLine in line]
        
        blocks = []
        for idx, start_idx in enumerate(start_lines):
            # if not the last one...
            if idx != len(start_lines)-1:
                blocks.append(user_data[start_idx:start_lines[idx+1]])
            else:
                # The last one
                blocks.append(user_data[start_idx:])
                
        
        logs_by_users[user] = []
        for block in blocks:
            #Get the question:
            first_line = block[0]
            #print "First line: " + first_line
            question = first_line[first_line.index(inputLine)+len(inputLine):]
            logtext = '\n'.join(block)
            correct = badResponse not in logtext
            bmods = modules_in_block(logtext)
            logs_by_users[user].append({"question": question, "modules": bmods, "correct": correct })
    
    return logs_by_users
    
    

def main():
    args = parser.parse_args()
    print dir(args)
    logs = open(args.logfile).read()
    
    log_result = break_logs(logs)
    print log_result


if __name__ == '__main__':
        main()