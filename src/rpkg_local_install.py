#!/usr/bin/env python
# coding: utf-8

import os
import o_p
import shutil
from call_cmd import call_cmd

def install(rpkg_tar_gz, dir_fpath):
    assert os.path.isdir(dir_fpath)
    def set_current(to_last):
        src = "last" if to_last else "previous"
        # :TRICKY: для переопределения сущ. ссылки нужно одновременно -f и -n ,-
        # артефакт *nix
        call_cmd("ln -s -f -n %s current" % src, cwd=dir_fpath)
    
    last_fpath = o_p.join(dir_fpath, "last")
    curr_fpath = o_p.join(dir_fpath, "current")
    if os.path.exists(last_fpath):
        curr_exists = False
        if os.path.exists(curr_fpath):
            assert os.path.islink(curr_fpath)
            curr_exists = True
        
        prev_fpath = o_p.join(dir_fpath, "previous")
        if os.path.exists(prev_fpath):
            shutil.rmtree(prev_fpath)
            
        shutil.move(last_fpath, prev_fpath)
        if curr_exists:
            set_current(False)
        
    os.mkdir(last_fpath)
    
    call_cmd("tar -xzf %(rpkg_tar_gz)s -C %(last_fpath)s" % locals())
    set_current(True)

if __name__ == '__main__':
    from parse_options import parse_args
    rpkg_tar_gz, dir_fpath = parse_args("rpkg.tar.gz", "local_dir")

    install(rpkg_tar_gz, dir_fpath)