
# -*- coding: utf-8 -*-

# std import
import os

# fief import
from fief import filter_effective_parameters as fief

# project import
from ..logger import log
from ..abcstep import StepStat
from .abcmapper import AbcMapper

class Hisat2(AbcMapper):
    """ Class for run mapper """

    def __init__(self):
        """ Intialize hisat2 runner object """
        super().__init__()

    @fief
    def read_configuration(self, mapper):
        """ Read the configuration object and prepare object to run """
        self.enable = mapper.getboolean("enable")
        self.name = mapper["name"]
        self.bin_path = mapper["bin_path"]
        self.in_path = mapper["in_path"]
        self.out_path = mapper["out_path"]
        self.index_path = mapper["index_path"]

        self.state = StepStat.load
    
    def check_configuration(self):
        """ Check if file, binary, other ressource is avaible for run mapper """

        if self.state != StepStat.load:
            log.debug("You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        if not self.enable :
            self.state = StepStat.no_ready
            return self.enable

        if not self.name.lower() == self.get_name().lower() : 
            self.state = StepStat.no_ready
                    
            log.debug("Mapper name is differente of classname we can't use this\
            class")
            return False

        if not os.path.isfile(self.bin_path) and os.access(self.bin_path,
                                                           os.X_OK) :
            self.state = StepStat.no_ready

            log.critical("Mapper binary file cannot be execute by you we can't \
            run mapping")
            return False

        # if not os.path.isfile(self.index_path) :
        #     self.state = StepStat.no_ready

        #     log.critical("index file cannot read by you we can't run mapping")
        #     return False

        if not os.path.isdir(self.in_path) :
            self.state = StepStat.no_ready

            log.critical("Path you set for in_path isn't a directory")
            return False

        if not os.path.isdir(self.out_path) :
            self.state = StepStat.no_ready

            log.critical("Path you set for out_path isn't a directory")
            return False

        self.state = StepStat.ready
        return True

    @fief
    def run(self):
        """ Run the mapper effectively """
        if self.state != StepStat.ready:
            log.debug("You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        base_command = [self.bin_path, "-x", self.index_path]
        for process in self._popen_run(base_command, input_flag="-q", output_flag="-S"):
            process.wait()
