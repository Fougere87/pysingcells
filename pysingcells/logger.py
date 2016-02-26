
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
    
    log_level = 10 if "logging_level" in options else options["logging_level"]
    log.setLevel(log_level)

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    log.addHandler(handler)


