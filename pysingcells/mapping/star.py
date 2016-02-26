
# -*- coding: utf-8 -*-

# project import
from .abcmapper import AbcMapper

class STAR(AbcMapper):
    """ Class for run mapper """

    def __init__(self):
        """ Intialize hisat2 runner object """
        super().__init__()
        self.input_flag = "--readFilesIn"
        self.output_flag = "--outFileNamePrefix"
        self.index_flag = "--genomeDir"
