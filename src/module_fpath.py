#!/usr/bin/env python
# coding: utf-8

import os, sys
import o_p

def get_mfpath(n, stack_depth=1):
    """ 0 - сам модуль, 1 - его директория, ... """
    def dn(fpath, n):
        for i in xrange(n):
            fpath = os.path.dirname(fpath)
        return fpath
    # путь модуля функции, которая вызвала get_mfpath()
    fpath = sys._getframe(stack_depth).f_globals["__file__"]
    # :TRICKY: половина из солидных python-приложений использует __file__ для
    # нахождения своего функционала из скрипта-точки входа; будем считать
    # это хорошей практикой
    # логи за пределами пакета
    return dn(os.path.realpath(fpath), n)

def get_mdir(stack_depth=1):
    """ 
    1 - непосредственный вызов get_mdir() из функции целевого модуля,
    2 - на вызов выше, и т.д.
    """
    # добавляем единицу для самой get_mdir()
    return get_mfpath(1, stack_depth+1)

def make_rel2abs(rel_fpath, stack_depth=1):
    """
    Построить абсолютный путь относительно пути модуля
    Значение stack_depth такое же, как и для get_mdir()
    """ 
    dir_fpath = get_mdir(stack_depth+1)
    return o_p.join(dir_fpath, rel_fpath)
