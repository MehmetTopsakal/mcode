

export PATH=$d/programs:$PATH
export PATH=$d/scripts/general:$PATH
export PATH=$d/scripts/python:$PATH
export PYTHONPATH=$d/scripts/python/mpy:$PYTHONPATH

export PATH=$d/scripts/local/think:$PATH

export PATH="/home/mt/software/anaconda3/bin:$PATH"

/home/mt/software/anaconda3/bin/jupyter notebook --no-browser > /dev/null 2> /dev/null &
sleep 1

