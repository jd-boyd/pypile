from __future__ import absolute_import, print_function

import os
import subprocess
import sys

import sexpdata
from sexpdata import Symbol

import nose2
import tempdir
#from nose2.tools import eq_

import compile

def eq_(a, b, comment=None):
    if comment:
        assert a==b, comment

    if a!=b:
        assert False, "%r != %r" % (a, b)

def test_return_immediate():
    td = ""
    compile.make_file(os.path.join(td, "test.s"),  0xdeadbeef)

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xdeadbeef\n")


def test_inc():
    td = ""
    compile.make_file(os.path.join(td, "test2.s"),  [Symbol("inc"), 0xdeadbeef])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test2.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xdeadbef0\n")

    
def test_add_cont():
    td = ""
    compile.make_file(os.path.join(td, "test2.s"),  
                      [Symbol("add"), 0xdeadbeef, 0xcafe])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test2.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xdeae89ed\n")

