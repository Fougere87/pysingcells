
# -*- coding: utf-8 -*-

# std import
from abc import ABCMeta, abstractmethod

# project import
from ..abcstep import AbcStep

class AbcMapper(AbcStep, metaclass=ABCMeta):
    """ Abstract class for mapper """
    
    def __init__(self):
        super().__init__()

    def get_name(self):
        """ Get the name of mapper """
        return self.__class__.__name__

