# -*- coding: UTF-8 -*-
import sys, os

root_folder = os.path.dirname(__file__) 

activate_this = '/var/www/wsgi/VEnvs/corpustester/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Add folder to path
sys.path.append(os.path.abspath(root_folder))

from corpustester import app as application
