Calista Log Parser
====================
Small phython utility to test the [Calista Bot](https://github.com/gsi-upm/calista-bot).

***WARNING: This is development level software.  Please do not use it unless you
             are familiar with what that means and are comfortable using that type
             of software.***

Corpus
---------------------------------------

An example csv corpus can be found in the "corpus" folder.

FE-test
---------------------------------------

Used to test the front-end controller (the "talkbot"), it can take several parameters, including
a corpus in csv format, and the controller url. It can work in strict mode, only accepting appropiate
responses as valid, or non-strict, accepting also gambits.
A small explanations of the command line parameters:

  | Param | Default  | Explanation |
  |  ------- | ---------- | ------------- |
  | -u URL, --url URL | http://localhost:8090 | URL to connect with the talkbot controller |
  | -c CORPUS, --corpus CORPUS | test_corpus.csv | CSV with the corpus |
  | -a AGENT, --agent AGENT | TestAgent | UserName to identify with the bot |
  | -v, --verbose | 0 | Verbosity level. -vvv equals a verbosity of 3 |
  | -s, --strict | 0 | Strict mode |
  | -o OUTPUT, --output OUTPUT | stdout | Where to log the results |
  | -h, --help | | Displays the help, and exits |


QA-test
---------------------------------------

Using a csv corpus, tests both ChatScript and SolR, withouth using the front-end controller.
It checks wether Chatscript recognizes the questions, returning and out-of-band command to retrieve
them from SolR, and wether doing a search of the question in solr returns a valid result.
It can take several command line arguments:

  | Param | Default  | Explanation |
  |  ------- | ---------- | ------------- |
  | -i IP, --ip IP | 127.0.0.1:1024 | Chatscript IP and Port |
  | -s SOLR, --solr SOLR | http://localhost:8080/solr/elearning | URL for the solr core |
  | -c CORPUS, --corpus CORPUS | test_corpus.csv | CSV with the corpus |
  | -a AGENT, --agent AGENT | TestAgent | UserName to identify with the bot |
  | -v, --verbose | 0 | Verbosity level. -vvv equals a verbosity of 3 |
  | -p, --premisive | 0 | Permisive mode (As oppose to strict) |
  | -o OUTPUT, --output OUTPUT | stdout | Where to log the results |
  | -h, --help | | Displays the help, and exits |


WSGI
---------------------------------------

For the QA-test, and WSGI script is provided, for use with Apache and mod_wsgi.
Keeping the directory structure, point the WSGIScriptAlias directive to the corpustester,
and provide an Alias for the static files.

The interface will allow to launch the test with the corpus, or input a custom question to be tested.


License
---------------------------------------
Copyright 2014 Alberto Mardomingo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


