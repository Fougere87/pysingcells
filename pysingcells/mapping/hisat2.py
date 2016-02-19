
# -*- coding: utf-8 -*-

# project import
from .abcmapper import AbcMapper

class Hisat2(AbcMapper):
    """ Class for run mapper """

    def __init__(self):
        """ Intialize hisat2 runner object """
        super().__init__()
        self.input_flag = "-q"
        self.output_flag = "-S"
        self.index_flag = "-x"

