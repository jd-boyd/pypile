from __future__ import absolute_import, print_function

import os
import subprocess
import sys

import sexpdata
from sexpdata import Symbol

import tempdir

import compile

def eq_(a, b, comment=None):
    if comment:
        assert a==b, comment

    if a!=b:
        assert False, "%r != %r" % (a, b)

def test_return_immediate():
    td = ""
    compile.make_file(os.path.join(td, "test.s"),  0xbeef)

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xbeef\n")


def test_inc():
    td = ""
    compile.make_file(os.path.join(td, "test2.s"),  [Symbol("inc"), 0xbeef])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test2.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xbef0\n")

def test_int_char():
    td = ""
    compile.make_file(os.path.join(td, "test3.s"),  [Symbol("int->char"), 1])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test3.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x43\n")

def test_char_int():
    td = ""
    compile.make_file(os.path.join(td, "test4.s"),  [Symbol("char->int"), "a"])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test4.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x61\n")


def test_add():
    td = ""
    compile.make_file(os.path.join(td, "test5.s"),  [Symbol("+"), 3, 4])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test5.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x7\n")


def test_add2():
    td = ""
    compile.make_file(os.path.join(td, "test6.s"),  [Symbol("+"), [Symbol("+"), 2, 3], 4])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test6.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x9\n")
    

    
# def test_add_cont():
#     td = ""
#     compile.make_file(os.path.join(td, "test2.s"),  
#                       [Symbol("add"), 0xdeadbeef, 0xcafe])

#     subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test2.s"), 
#                     shell=True)

#     ret = subprocess.check_output("./a.out")
#     eq_(ret, b"ret 0xdeae89ed\n")

