import sys, os, socket
import subprocess as sp


overwrite = True


hostname = socket.gethostname()


if hostname == 'lnc-170365':
    
    if overwrite:
        
        # subprocess.run('jupyter lab --generate-config', shell=True)
        if os.path.exists('jupyter_lab_config_lnc-170365.py'): os.remove('jupyter_lab_config_lnc-170365.py')
        sp.run('echo "c.ContentsManager.allow_hidden = True" >>  jupyter_lab_config_lnc-170365.py', shell=True)
        sp.run('echo "c.NotebookApp.port = 8888" >>  jupyter_lab_config_lnc-170365.py', shell=True)
        sp.run('echo "c.LabServerApp.open_browser = False" >>  jupyter_lab_config_lnc-170365.py', shell=True)
        os.makedirs('/home/mt/.jupyter/_ipynb_checkpoints',exist_ok=True)
        sp.run('echo "c.FileCheckpoints.checkpoint_dir = /home/mt/.jupyter/_ipynb_checkpoints" >>  jupyter_lab_config_lnc-170365.py', shell=True)
        
    sp.run('ln -fs /home/mt/mcode/_etc/jupyter_lab_config_lnc-170365.py /home/mt/.jupyter/jupyter_lab_config.py ', shell=True)









if hostname == 'matsci.dne.bnl.gov':

    if overwrite:
        
        # subprocess.run('jupyter lab --generate-config', shell=True)
        if os.path.exists('jupyter_lab_config_matsci.py'): os.remove('jupyter_lab_config_matsci.py')
        sp.run('echo "c.ContentsManager.allow_hidden = True" >>  jupyter_lab_config_matsci.py', shell=True)
        sp.run('echo "c.NotebookApp.port = 10000" >>  jupyter_lab_config_matsci.py', shell=True)
        sp.run('echo "c.LabServerApp.open_browser = False" >>  jupyter_lab_config_matsci.py', shell=True)
        os.makedirs('/home/mtopsakal/.jupyter/_ipynb_checkpoints',exist_ok=True)
        sp.run('echo "c.FileCheckpoints.checkpoint_dir = /home/mtopsakal/.jupyter/_ipynb_checkpoints" >>  jupyter_lab_config_matsci.py', shell=True)
        
    sp.run('ln -fs /home/mtopsakal/mcode/_etc/jupyter_lab_config_matsci.py /home/mtopsakal/.jupyter/jupyter_lab_config.py ', shell=True)
        
    
    
    
    
    
    













