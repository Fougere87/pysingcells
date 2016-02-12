import configparser
from subprocess import call
import os

config = configparser.ConfigParser()

config.read('params.cfg')
print(config.sections())

for key in config['steps']: print(config['steps'][key])


def trimming(files_dir, rep_out , paired=1) :
    file_list = os.listdir(files_dir)
    for fastq in file_list :
        call(['cmd', 'options...'])
