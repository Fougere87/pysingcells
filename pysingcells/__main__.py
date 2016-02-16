#!/usr/bin/env python3

# std import
import os
import sys
import configparser
from subprocess import call

# project import
from . import logger
from .mapper import hisat2


def main(config_path):
    """ Main function of pro'gramme read configuration and run enable step """
    config = configparser.ConfigParser()

    logger.setup_logging(**config)

    config.read(config_path)
    print(config.sections())

    for key in config['paths']: print(config['paths'][key])


def trimming(files_dir, rep_out , paired=1) :
    file_list = os.listdir(files_dir)
    for fastq in file_list :
        call(['cmd', 'options...'])


if __name__ == "__main__":
    main(sys.argv[1])
