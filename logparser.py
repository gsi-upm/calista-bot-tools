#!/usr/bin/python

import sys
import re

# List of modules, by the name it can be identified in the log
modules = ['Unitex', 'ChatScript', 'SIREN', 'JASON']

# Input "flag"
# The line that identifies the first line of a new question-answer block
inputLine = "Unitex input: "


def modules_in_block(block):
    """
    Find what modules intervene in a given question-answer block
    """
    logtext = '\n'.join(block)
    mods = []
    #Search for each module
    for mod in modules:
        if mod in logtext:
            mods.append(mod)
    print mods
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
        print user
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
            bmods = modules_in_block(block)
            logs_by_users[user].append({"question": question, "modules": bmods})
    
    return logs_by_users
    
    

def main(logfile, outfile):
    logs = open(logfile).read()
    
    print break_logs(logs)


if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print "Usage logparser.py LOG_FILE OUT_FILE "
        sys.exit(0)
        
    main(sys.argv[1], sys.argv[2])