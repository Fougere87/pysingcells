
# -*- coding: utf-8 -*-

# std import
import os
import json
from enum import Enum
from abc import ABCMeta, abstractmethod

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
            "stdout": process.stdout.read(),
            "stderr": process.stderr.read()
        }

        with open(os.path.join(self.log_dir, name), 'w') as log_file:
            json.dump(log, log_file)

