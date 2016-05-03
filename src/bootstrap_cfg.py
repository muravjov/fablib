#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

cfg = None

def init(hook_func=None):
    args = None
    
    global cfg
    if not cfg:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-c', '--config',
            dest='config', type=str, 
            required=True, # default=,
            help='path to configuration file',
        ) 
        
        if hook_func:
            hook_func(parser)
        
        args = parser.parse_args()
        import yaml
        with open(args.config) as f:
            cfg = yaml.load(f)
            
    return args

def get_cfg_value(key, def_value=None):
    return cfg.get(key, def_value)

#
#
#
import logging

def setup_handler(handler, level, logger, is_colored=False):
    handler.setLevel(level)
    
    # :TODO: would like to have colored output like 
    # Ivan Egorov does
    #formatter = Formatter(color=is_colored)
    formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)

def setup_file_handler(logger, fpath, level, is_append=False):
    f = logging.FileHandler(
        fpath,
        mode= "a" if is_append else "w"
    )
    
    setup_handler(f, level, logger, False)
    
def setup_console_logger(logger, logging_level):
    ch = logging.StreamHandler()

    setup_handler(ch, logging_level, logger, True)
    return ch
    
def setup_logger(logger, fpath, logging_level, is_append=True):
    logger.setLevel(logging_level)
    setup_console_logger(logger, logging_level)
    setup_file_handler(logger, fpath, logging_level, is_append=is_append)
