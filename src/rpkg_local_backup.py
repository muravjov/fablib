#!/usr/bin/env python
# coding: utf-8

import o_p
from call_cmd import call_cmd

if __name__ == '__main__':
    from parse_options import parse_args
    dir_fpath, tar_fname = parse_args("local_dir", "tar_fname")

    if o_p.exists(tar_fname):
        res = o_p.remove_file(tar_fname)
        assert res

    # :REFACTOR:
    call_cmd("tar -cf %(tar_fname)s -C %(dir_fpath)s ." % locals())
    