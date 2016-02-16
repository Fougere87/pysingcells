
# -*- coding: utf-8 -*-

# std import
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


