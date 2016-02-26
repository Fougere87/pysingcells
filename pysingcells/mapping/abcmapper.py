
# -*- coding: utf-8 -*-

# std import
import os
import subprocess
from abc import ABCMeta

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

class AbcMapper(AbcStep, metaclass=ABCMeta):
    """ Abstract class for mapper """
    
    def __init__(self):
        """ Intilize mapper """
        super().__init__()
        self.name = ""
        self.bin_path = ""
        self.index_path = ""
        self.in_path = ""
        self.out_path = ""
        self.options = ""
        self.input_flag = ""
        self.output_flag = ""
        self.index_flag = ""

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

    def run(self):
        """ Run the mapper effectively """

        log.info(self.get_name() + " run")

        if self.state != StepStat.ready:
            log.debug(" You are not in the good state to run this, maybe you \
            have a problem.")
            return False

        base_command = [self.bin_path, self.index_flag, self.index_path]
        base_command += self.options.split(" ")

        for (arg, name, process) in self._popen_run(base_command,
                                                    input_flag=self.input_flag,
                                                    output_flag=
                                                    self.output_flag):
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
