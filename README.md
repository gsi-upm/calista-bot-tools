Calista Log Parser
====================
Small phython utility to parse the logs from the [Calista Bot](https://github.com/gsi-upm/calista-bot) into a format to generate plotable data.

***WARNING: This is development level software.  Please do not use it unless you
             are familiar with what that means and are comfortable using that type
             of software.***

Usage
---------------------------------------


How it works
---------------------------------------

Given a log file, it will break the log by pieces of conversation (question - answer), and
sort it by user, given the data break down per user.

For each response, it will provide a timestamp, que question and answer, and a list of the modules that
contributed to said answer.

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


