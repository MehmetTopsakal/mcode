# mount google drive
import sys,os, subprocess
from google.colab import drive,files
drive.mount('/drive')
subprocess.call('ln -s /drive/My\ Drive '+os.environ['HOME']+'/gd', shell=True);
