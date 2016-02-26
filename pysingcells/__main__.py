#!/usr/bin/env python3

# std import
import sys
import string
import pkgutil
import configparser

# string-utils import
import string_utils

# project import
from . import logger
from .abcstep import StepStat

def main(config_path):
    """ Main function of programme read configuration and run enable step """
    config = configparser.ConfigParser(interpolation =
                                       configparser.ExtendedInterpolation())

    config.read(config_path)

    logger.setup_logging(**config)

    for step_name in config['options']['steps'].split(","):
        if step_name in [modname for importer, modname, ispkg in 
                         pkgutil.iter_modules(
                             sys.modules[__package__].__path__)]:

            appli_name = config[step_name]['name']

            module_step = __import__(".".join(["pysingcells", step_name]),
                                     fromlist="pysingcells")

            if appli_name.lower() in [modname for importer, modname, ispkg in
                              pkgutil.iter_modules(module_step.__path__)]:

                appli_module = __import__(".".join(["pysingcells", step_name, 
                                                    appli_name.lower()]),
                                          fromlist=".".join(["pysingcells", 
                                                             step_name]))

                appli_class = getattr(appli_module,
                                      snake_case_to_capword(appli_name))
                appli_instance = appli_class()
                appli_instance.read_configuration(**config)

                if appli_instance.check_configuration():
                    appli_instance.run()

                    if appli_instance.state != StepStat.succes:
                        logger.log.warning(appli_name + " failled current run see log file")
                        exit(1)
                else:
                    logger.log.warning(appli_name +
                                       " failled in check her conf")
            else:
                logger.log.warning(appli_name +
                                   " isn't avaible in pysingcells." + step_name)
        else:
            logger.log.warning(step_name + " isn't avaible in pysingcells")


def snake_case_to_capword(base):
    if not string_utils.is_snake_case(base) or base.isupper():
        base = "".join(c.upper() if i == 0 else c for i, c in enumerate(base))
        return base

    return string_utils.snake_case_to_camel(base).title()

if __name__ == "__main__":
    main(sys.argv[1])
