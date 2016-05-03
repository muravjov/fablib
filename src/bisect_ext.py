#!/usr/bin/env python
# coding: utf-8

# Расширение функций bisect из-за пользовательской less_op

def builtin_less(x1, x2):
    return x1 < x2

def bisect_left(a, x, lo=0, hi=None, less_op=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    if less_op is None:
        less_op = builtin_less

    while lo < hi:
        mid = (lo+hi)//2
        if less_op(a[mid], x):
            lo = mid+1
        else:
            hi = mid
    return lo

def bisect_right(a, x, lo=0, hi=None, less_op=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    if less_op is None:
        less_op = builtin_less
        
    while lo < hi:
        mid = (lo+hi)//2
        if less_op(x, a[mid]):
            hi = mid
        else:
            lo = mid+1
    return lo
