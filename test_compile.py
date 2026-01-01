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


def test_add3():
    td = ""
    compile.make_file(os.path.join(td, "test7.s"),  [Symbol("+"), [Symbol("+"), 2, 3],  [Symbol("+"), 4, 6]])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test7.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xf\n")
    

def test_mull():
    td = ""
    compile.make_file(os.path.join(td, "test8.s"),  [Symbol("*"), 3,  4])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test8.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xc\n")
    
def test_let():
    td = ""
    compile.make_file(os.path.join(td, "test9.s"),  [Symbol("let"), [[Symbol("bob"), 5]],  6])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test9.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x6\n")

def test_var():
    td = ""
    compile.make_file(os.path.join(td, "test10.s"),  [Symbol("let"), [[Symbol("bob"), 5]],  Symbol("bob")])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test10.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x5\n")

def test_var2():
    td = ""
    compile.make_file(os.path.join(td, "test11.s"),  [Symbol("let"), [[Symbol("bob"), 5]],  [Symbol("+"), 2, Symbol("bob")]])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test11.s"), 
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x7\n")


def test_var2():
    td = ""
    compile.make_file(os.path.join(td, "test12.s"),
                      [Symbol("let"), [[Symbol("bob"), 5],
                                       [Symbol("fred"), 3]],
                       [Symbol("+"), Symbol("fred"), Symbol("bob")]])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test12.s"),
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x8\n")


def test_if_true():
    td = ""
    compile.make_file(os.path.join(td, "test13.s"),
                      [Symbol("if"), True, 10, 20])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test13.s"),
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0xa\n")


def test_if_false():
    td = ""
    compile.make_file(os.path.join(td, "test14.s"),
                      [Symbol("if"), False, 10, 20])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test14.s"),
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x14\n")


def test_if_nested():
    td = ""
    compile.make_file(os.path.join(td, "test15.s"),
                      [Symbol("if"), True,
                       [Symbol("if"), False, 1, 2],
                       3])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test15.s"),
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x2\n")


def test_if_with_let():
    td = ""
    compile.make_file(os.path.join(td, "test16.s"),
                      [Symbol("let"), [[Symbol("x"), 5]],
                       [Symbol("if"), False, Symbol("x"), [Symbol("+"), Symbol("x"), 1]]])

    subprocess.call("gcc -g cref/main.c " + os.path.join(td, "test16.s"),
                    shell=True)

    ret = subprocess.check_output("./a.out")
    eq_(ret, b"ret 0x6\n")
