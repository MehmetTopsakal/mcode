import os.path
import shutil

def set_defaults(name, val):
    ''' set a global variable.'''
    global t4iss_defaults
    t4iss_defaults[name] = val

def print_defaults():
    for key, val in t4iss_defaults.items():
        print("- {} : {}".format(key, val))


# essential imports
import numpy as np
import os,sys,shutil,subprocess,pickle
from os.path import join



here   = os.path.dirname(os.path.realpath(__file__))

user_home = os.path.expanduser('~')

if not os.path.isdir(os.path.join(user_home,'.t4iss')):
    os.mkdir(os.path.join(user_home,'.t4iss'))
    os.mkdir(os.path.join(user_home,'.t4iss','xanes_data'))
    os.mkdir(os.path.join(user_home,'.t4iss','scratch'))
    
# defaults
t4iss_defaults  = dict()
t4iss_defaults['t4iss_xanes_data'] = os.path.join(user_home,'.t4iss','xanes_data')
t4iss_defaults['t4iss_scratch'] = os.path.join(user_home,'.t4iss','scratch')
t4iss_defaults['mcr_path'] = os.path.join(here,'mcr')
t4iss_defaults['scripts_path'] = os.path.join(here,'scripts')
t4iss_defaults['octave_path'] = shutil.which('octave')
t4iss_defaults['matlab_path'] = shutil.which('matlab')

print("\nImported t4iss with defaults:\n")
print_defaults()
