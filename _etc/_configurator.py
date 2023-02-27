import sys, os, socket
import subprocess as sp


overwrite = True


hostname = socket.gethostname()


if hostname == 'lnc-170365':
    
    if overwrite:
        
        # subprocess.run('jupyter lab --generate-config', shell=True)
        if os.path.exists('jupyter_lab_config.py'): os.remove('jupyter_lab_config.py')
        sp.run('echo "c.ContentsManager.allow_hidden = True" >>  jupyter_lab_config.py', shell=True)
        sp.run('echo "c.NotebookApp.port = 8888" >>  jupyter_lab_config.py', shell=True)
        sp.run('echo "c.LabServerApp.open_browser = False" >>  jupyter_lab_config.py', shell=True)
        os.makedirs('/home/mt/.jupyter/_ipynb_checkpoints',exist_ok=True)
        sp.run('echo "c.FileCheckpoints.checkpoint_dir = /home/mt/.jupyter/_ipynb_checkpoints" >>  jupyter_lab_config.py', shell=True)
        
    sp.run('ln -fs /home/mt/code/_etc/jupyter_lab_config.py /home/mt/.jupyter/jupyter_lab_config.py ', shell=True)
        
    
    
    
    
    
    













