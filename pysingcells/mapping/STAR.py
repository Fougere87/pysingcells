
# -*- coding: utf-8 -*-

# std import
import os

# fief import
from fief import filter_effective_parameters as fief

# project import
from ..logger import log
from ..abcstep import StepStat
from .abcmapper import AbcMapper

class STAR(AbcMapper):
    """ Class for run mapper """

    def __init__(self):
        """ Intialize hisat2 runner object """
        super().__init__()

    @fief
    def read_configuration(self, mapping):
        """ Read the configuration object and prepare object to run """

        log.info(self.get_name() + " read configuration")

        self.name = mapping["name"]
        self.bin_path = mapping["bin_path"]
        self.in_path = mapping["in_path"]
        self.out_path = mapping["out_path"]
        self.index_path = mapping["index_path"]
        self.log_dir = mapping["log"]
        self.options = mapping["options"]

        self.state = StepStat.load
    
    def check_configuration(self):
        """ Check if file, binary, other ressource is avaible for run mapper """

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

        if not os.path.isfile(self.bin_path) and os.access(self.bin_path,
                                                           os.X_OK) :
            self.state = StepStat.no_ready

            log.critical("Mapper binary file cannot be execute by you we can't \
            run mapping")
            return False

        if not os.path.isdir(os.path.dirname(self.index_path)) :
            self.state = StepStat.no_ready

            log.critical("Index file cannot read by you we can't run mapping")
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


        self.state = StepStat.ready
        return True

    @fief
    def run(self):
        """ Run the mapper effectively """
        
        log.info(self.get_name() + " run")

        if self.state != StepStat.ready:
            log.debug(" You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        base_command = [self.bin_path, "--genomeDir", self.index_path,
                        self.options]

        for (arg, name, process) in self._popen_run(base_command,
                                                    input_flag="--readFilesIn",
                                                    output_flag=
                                                    "--outFileNamePrefix"):
            process.wait()

            if process.returncode != 0:
                log.warning(self.get_name() + " process " + name +
                            " failed see log dir.")
                self.state = StepStat.failled
            else:
                log.info(self.get_name() + " process " + name +
                         " sucess")
                self.state = StepStat.succes

            self._write_process(arg, name, process)
        
