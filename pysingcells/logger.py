
# -*- coding: utf-8 -*-

""" Function related to logging """

# stp import
import sys
import logging

# fief import
from fief import filter_effective_parameters as fief

log = logging.getLogger()

@fief
def setup_logging(options):
    
    log.setLevel(10 if "logging_level" in options else
                 options["logging_level"])

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(levelname)s :: %(message)s'))
    handler.setLevel(10 if "logging_level" in options else
                     options["logging_level"])

    log.addHandler(logging.StreamHandler(sys.stderr))


