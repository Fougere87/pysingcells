
# -*- coding: utf-8 -*-

# std import
import os
from abc import ABCMeta, abstractmethod

# fief import
from fief import filter_effective_parameters as fief

# project import
from ..logger import log
from ..abcstep import AbcStep, StepStat

# tested import
try:
    from os import scandir
except ImportError:
    from scandir import scandir

class AbcCounting(AbcStep, metaclass=ABCMeta):
    """ Abstract class for mapper """
    
    def __init__(self):
        """ Initiliaze couting """
        super().__init__()
        self.name = ""
        self.bin_path = ""
        self.in_path = ""
        self.out_path = ""
        self.log_dir = ""
        self.options = ""
        self.annotation_path = ""
        self.compute_norm = "tpm"

        # command flag
        self.annotation_flag = ""
        self.input_flag = ""
        self.output_flag = ""

    @fief
    def read_configuration(self, counting):
        """ read configuration of counting """
        
        log.info(self.get_name() + " read configuration")

        self.name = counting["name"]
        self.bin_path = counting["bin_path"]
        self.in_path = counting["in_path"]
        self.out_path = counting["out_path"]
        self.log_dir = counting["log"]
        self.options = counting["options"]
        self.annotation_path = counting["annotation_path"]
        self.compute_norm = counting["compute_norm"]

        self.state = StepStat.load

    def check_configuration(self):
        """ Check if file, binary, other ressource is avaible for run count """

        log.info(self.get_name() + " check configuration")

        if self.state != StepStat.load:
            log.critical("You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        if not self.name.lower() == self.get_name().lower() :
            self.state = StepStat.no_ready

            log.critical("Mapper name is differente of classname we can't use \
            this class")
            return False

        if not os.path.isdir(self.in_path) :
            self.state = StepStat.no_ready

            log.critical("Path you set for in_path isn't a directory")
            return False

        if not os.path.isdir(self.out_path) :
            self.state = StepStat.no_ready

            log.critical("Path you set for out_path isn't a directory")
            return False

        if not os.path.isdir(self.log_dir) :
            self.state = StepStat.no_ready

            log.critical("Path you set for log_dir isn't a directory")
            return False

        if not os.path.isfile(self.annotation_path):
            self.state = StepStat.no_ready

            log.critical("Path you set for annotation_path isn't a file")
            return False

        self.state = StepStat.ready
        return True
            
    def run(self):
        """ Run the counting effectively """

        log.info(self.get_name() + " run")

        if self.state != StepStat.ready:
            log.debug(" You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        if self._run_counting() and self._convert_output():
            self.state = StepStat.succes
        else:
            self.state = StepStat.failled

    def get_name(self):
        """ Get the name of mapper """
        return self.__class__.__name__

    @abstractmethod
    def _run_counting(self):
        """ Run counting effectively """
        pass

    @abstractmethod
    def _convert_output(self):
        """ Convert output in useful format """
        pass

def tpm(count, length, nb_read):
    """ Return the tpm value """
    length /= 10**3
    pm = nb_read / (10**6)
    rpk = count / length

    return rpk / pm


def rpkm(count, length, nb_read):
    """ Return the rpkm value """
    length /= 10**3
    pm = nb_read / (10**6)
    rpm = count / pm
    return rpm / length

def rpm(count, _, nb_read):
    """ Return rpm value """
    return (count / nb_read) * 10**6
