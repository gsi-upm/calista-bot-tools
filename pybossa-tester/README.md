# CalistaBot test module for pybossa

This is a small set of tasks to test the calista bot at http://demos.gsi.dit.upm.es/gsibot/

## Setting up the tasks

You need to have pybossa-pbs already configured. For more info on this, check the [pbs documentation](http://docs.pybossa.com/en/latest/user/pbs.html).

Edit the project.json file and add the relevant data.
```json
{
    "name": "Calista-Bot-tester",
    "short_name": "calistabottest",
    "description": "Q-A",
    "question": "Is this answer correct?"
}
```
Create the project:
```bash
    $ pbs create_project
```

In other to get the tasks, edit the qlist.txt file with the set of questions you want to test, and run the "get_answers.py" script, specifying the talkbot server:
```bash
    $ ./get_answers.py bot_url > bot_tasks.json
```

This will generate generic-questions tasks, that you can add to the project, along with the templates:
```bash
    $ pbs add_tasks --tasks-file bot_tasks.json --tasks-type=json
    $ pbs update_project
```

You will now be able to see the project in the pybossa interface, and start working on the tasks.

## Acknowledgments

This module is based on the [Flickrperson module](https://github.com/PyBossa/app-flickrperson) from Pybossa, following their doc on how to [create pybossa tasks](http://docs.pybossa.com/en/latest/user/tutorial.html).


## License


Copyright (C) 2014  Albert Mardomingo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.