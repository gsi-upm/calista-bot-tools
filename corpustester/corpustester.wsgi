# -*- coding: UTF-8 -*-
import sys, os

# Add folder to path
root_folder = os.path.dirname(__file__) 
sys.path.append(os.path.abspath(root_folder))

from corpustester import app as application
