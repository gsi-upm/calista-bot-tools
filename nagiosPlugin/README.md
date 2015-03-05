Calista Nagios Plugin
====================
Nagios Plugin to check test the [Calista Bot](https://github.com/gsi-upm/calista-bot)

***WARNING: This is development level software.  Please do not use it unless you
             are familiar with what that means and are comfortable using that type
             of software.***

Usage
---------------------------------------
Install it in your nagiosplugins folder. It takes as command line parameter the url of the talkbot controller.

How it works
---------------------------------------

It will send two questions to the bot ("Hola" and "que es un for"), with an user "nagiosUser", and check the response
Return codes:
    
    * 0 : Both responses where valid
    * 1 : The first request got a response, but the second one did not
    * 2 : Neither request got a response, the bot is down.

License
---------------------------------------
Copyright 2015 Alberto Mardomingo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


