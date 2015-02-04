from __future__ import absolute_import, print_function

import os
import subprocess
import sys

import sexpdata
from sexpdata import Symbol

import nose2
import tempdir
#from nose2.tools import eq_

import loader

def print_file(ret):
    print()
    print("\n".join(repr(r) for r in ret.functions.values()))

def test_parse_onefun():
    s = """
(define (d e f) (+ e f))
"""

    ret = loader.load_file(s)
    print_file(ret)
    #assert False


def test_parse_twofun():
    s = """
(define (a b c) 5)

(define (d e f) (+ e f))
"""

    ret = loader.load_file(s)
    print_file(ret)
    #assert False
