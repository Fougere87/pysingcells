
# -*- coding: utf-8 -*-

""" Function related to logging """

# stp import
import sys
import logging

# fief import
from fief import filter_effective_parameters as fief

@fief
def setup_logging(options):
    
    log = logging.getLogger()

    log.setLevel(10 if "logging_level" in options else options["logging_level"])
    log.addHandler(logging.StreamHandler(sys.stderr))

log = logging.getLogger()
