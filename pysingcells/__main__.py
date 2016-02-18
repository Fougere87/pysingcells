#!/usr/bin/env python3

# std import
import os
import sys
import configparser
from subprocess import call

# project import
from . import logger
from .mapping import hisat2

def main(config_path):
    """ Main function of programme read configuration and run enable step """
    config = configparser.ConfigParser(interpolation =
                                       configparser.ExtendedInterpolation())

    config.read(config_path)

    logger.setup_logging(**config)

    for key in config['options']['steps'].split(","):
        for key2 in config[key]:
            print(key2 + ' : ' + config[key][key2])

def trimming(files_dir, rep_out , paired=1) :
    file_list = os.listdir(files_dir)
    for fastq in file_list :
        call(['cmd', 'options...'])


if __name__ == "__main__":
    main(sys.argv[1])
