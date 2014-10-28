#!/usr/bin/python

from __future__ import print_function
import sys
import argparse

import time
import datetime
import re

import csv
import json

# The command line options:
# The arguments I can take:
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plottable", help="Print the data in a csv (plottable-friendly) format",
                    action="store_true")
parser.add_argument("-n", "--noerrors", help="Do not include the errors",
                    action="store_true")
    
# The log input/oputput
parser.add_argument("-l", "--logfile", type=str, help="The file with the logs",
                    required=True)
parser.add_argument("-o", "--outfile", help="If specified, write the result to the file")

# How shall I group the arguments for the plot?
# Defaults to hourly
parser.add_argument("-t", "--timegroup", type=str, default="hour",
                    choices=["hour", "day", "week" "month"],
                    help="The time periods to group the arguments. Defaults to hourly")

# Modules, by the name it can be identified in the log
modules = {'unitex': 'Unitex', 'cs':'ChatScript', 'siren':'SIRENSLog', 'jason': 'JASONLog'}

# Input "flag"
# The line that identifies the first line of a new question-answer block
inputLine = "Unitex input: "

# The answer when the bot doesn't know how to respond.
badResponse = "Hey, sorry. What were we talking about?"

# I'm going to use this a fair number of times, so I compile it beforehand
time_re = re.compile("^(\w+\s\d{1,2}\s\d{1,2}:\d{2})")

# The headers for the csv
csv_headers = ["User", "ResponseModule", "Question", "Correct", "Timestamp"]

def response_module(logtext):
    """
    Find what modules intervene in a given question-answer block
    """
    if modules['siren'] in logtext:
        return "SIREN"
    return "ChatScript"

def get_time(first_line):
    """
    Given the first line of the logs, return a datetime object
    """
    timestamp = time_re.search(first_line).group(1)
  
    # I know the date format is "Month, day, hour:minutes", so...
    # (Probably a better idea would be adding a config or something)
    # Also, let's cheat a little, shall we?
    # The current log format does NOT include year, so I'll assume we
    # are talking about the current year:
    year = datetime.date.today().strftime("%Y")

    t_strc = time.strptime(year +" " +timestamp, "%Y %b %d %H:%M")
    return datetime.datetime.fromtimestamp(time.mktime(t_strc))

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
            rmod = response_module(logtext)
            logs_by_users[user].append({"question": question, "module": rmod, "correct": correct,
                                        "time": get_time(first_line).isoformat()})
    
    return logs_by_users
    
def plotable_data(log_dict):
    """
    Converts the log to a plotable format
    """
    # The header
    csv_data = ", ".join(csv_headers)
    
    # Parse the data
    for user, value in log_dict.iteritems():
        for row in value:
            # TODO: Should I check for commas in the data?
            # Place the linebreak only if necesary.
            csv_data += "\r\n{user}, {module}, {question}, {correct}, {timestamp}".format(
                user=user, module=row['module'], question=row["question"],
                correct=row['correct'], timestamp=row["time"])
    
    return csv_data

def main():
    
    # Anything we do, first we get the arguments and parse the logfile
    args = parser.parse_args()
    logs = open(args.logfile).read()
    l_data = break_logs(logs)

    # Now, how do we want to present the results?
    log = plotable_data(l_data) if args.plottable else json.dumps(l_data, indent=4)
    
    # File or stdout?
    out = open(args.outfile, "w") if args.outfile else sys.stdout
    print(log, file=out)


if __name__ == '__main__':
        main()