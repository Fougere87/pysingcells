
# -*- coding: utf-8 -*-

# std import
import os
import json
import subprocess
from enum import Enum
from abc import ABCMeta, abstractmethod

# tested import
try:
    from os import scandir
except ImportError:
    from scandir import scandir

class StepStat(Enum):
    nostat = 1
    load = 2
    no_ready = 3
    ready = 4
    succes = 5
    failled = 6

class AbcStep(metaclass=ABCMeta):
    """ Abstract class for mapper """

    def __init__(self):
        self.state = StepStat.nostat
        self.name = ""
        self.bin_path = ""
        self.index_path = ""
        self.in_path = ""
        self.out_path = ""
        self.options = ""
        self.log_dir = ""

    @abstractmethod
    def read_configuration(self, configuration):
        """ Read the configuration object and prepare object to run """
        pass

    @abstractmethod
    def check_configuration(self):
        """ Check if file, binary, other ressource is avaible for run mapper """
        pass

    @abstractmethod
    def run(self):
        """ Run the step effectively """
        pass

    def get_name(self):
        """ Get the name of mapper """
        return self.__class__.__name__

    def _write_process(self, argument, name, process):
        """ Write step log in log_dir """
        log = {
            "cmd": " ".join(argument),
            "stdout": process.stdout.read().decode(),
            "stderr": process.stderr.read().decode()
        }

        with open(os.path.join(self.log_dir, name), 'w') as log_file:
            json.dump(log, log_file)

    def _popen_run(self, base_cmd, input_flag="-i", output_flag="-o"):
        """ generator of popen subprocess to run mapper """

        for read_name in scandir(self.in_path):
            if not read_name.is_dir():
                read_name = read_name.name
                second_part = list()
                second_part.append(input_flag)
                second_part.append(os.path.join(self.in_path, read_name))
                second_part.append(output_flag)
                second_part.append(os.path.join(self.out_path, read_name))

                process = subprocess.Popen(base_cmd + second_part,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

                yield (base_cmd + second_part, read_name, process)
