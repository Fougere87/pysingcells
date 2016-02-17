
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
        """ Run the mapper effectively """
        pass

    def _write_process(self, log_dir, process):
        """ Write step log in log_dir """
        log = {
            "cmd": " ".join(process.argument),
            "stdout": process.stdout.read().decode(),
            "stderr": process.stderr.read().decode()
        }

        with open(os.path.join(log_dir, process.name), 'w') as log_file:
            json.dump(log, log_file)
