
# -*- coding: utf-8 -*-

# std import
import os
import subprocess
from abc import ABCMeta, abstractmethod

# project import
from ..abcstep import AbcStep

# tested import
try:
    from os import scandir
except ImportError:
    from scandir import scandir

class AbcMapper(AbcStep, metaclass=ABCMeta):
    """ Abstract class for mapper """
    
    def __init__(self):
        super().__init__()
        self.enable = False
        self.name = ""
        self.bin_path = ""
        self.index_path = ""
        self.in_path = ""
        self.out_path = ""

    def get_name(self):
        """ Get the name of mapper """
        return self.__class__.__name__

    def _popen_run(self, base_cmd, input_flag="-i", output_flag="-o"):
        """ generator of popen subprocess to run mapper """

        for read_name in scandir(self.in_path):
            if not read_name.is_dir():
                second_part = list()
                second_part.append(input_flag)
                second_part.append(os.path.join(self.in_path, read_name.name))
                second_part.append(output_flag)
                second_part.append(os.path.join(self.out_path, read_name.name))

                process = subprocess.Popen(base_cmd + second_part,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

                process.argument = base_cmd + second_part
                process.name = read_name.name

                yield process
