from __future__ import absolute_import, print_function

import sexpdata
from sexpdata import Symbol

# 1. return numbers
# 2. Math
# 3. logic
# 4. functions
# 5. FFI

#gcc -O0 -S -fomit-frame-pointer

#(define (fun1 x y)
# (+ x y))

# arg register order:  RDI, RSI, RDX, RCX, R8, and R9
# Then stack: 
#	movl	$10, 8(%rsp)
#	movl	$9, (%rsp)
# or pushq/popq (q for 64bit)

# RBP, RBX, and R12-R15 are callee-save registers; 
# all others must be saved by the caller if they wish to preserve their values.[


def file_preamble(fh):
    fh.write("""        .file   "two_func.c"
        .text
""")


def file_postamble(fh):
    fh.write("""        .ident  "GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
        .section        .note.GNU-stack,"",@progbits
""")


FIXNUM_MASK = 0b11
FIXNUM_TAG = 0
FIXNUM_SHIFT = 2

CHAR_MASK = 0b11111111
CHAR_TAG =  0b00001111
CHAR_SHIFT = 8

BOOL_MASK = 0b1111111
BOOL_TAG =  0b0011111
BOOL_SHIFT = 7

EMPTY_MASK = 0b11111111
EMPTY_TAG =  0b00101111
EMPTY_SHIFT = 8

def emit(fh, instruction):
    fh.write("        " + instruction + "\n")
        

def emit_expr(fh, x):
    print("emit_expr:", repr(x))
    if is_immediate(x):
        emit(fh, "mov ${0}, %eax".format(immediate_rep(x)))
        return
    if not is_call(x):
        assert False, "If not primitive, must be call."

    if is_primcall(x):
        PRIM_CAL_DICT[x[0].tosexp()](fh, x[1:])
        return
        
    assert False, "Couldn't figure out what to emit"


def emit_null(x):
    pass


def emit_zero(x):
    pass


def emit_int_char(fh, x):
    emit_expr(fh, x[0])
    emit(fh, "sall $6, %eax")
    emit(fh, "orl $15, %eax")


def emit_char_int(fh, x):
    print("emit_char_int(", x, ")")
    emit_expr(fh, x[0])
    emit(fh, "sarl $8, %eax")
    emit(fh, "sall $2, %eax")


def emit_inc(fh, l):
    print("emit_inc")
    emit_expr(fh, l[0])
    emit(fh, "addl ${0}, %eax".format(immediate_rep(1)))


def emit_mul(fx, x):
    pass
 

def emit_add(fh, x):
    assert len(x) == 2
    print("emit add")
    emit_expr(fh, x[1])
    #emit(fh, "movq %rax, -8(%rsp)")
    emit(fh, "pushq %rax")
    emit_expr(fh, x[0])
    emit(fh, "popq %rdx")
    emit(fh, "addq   %rdx, %rax")
 
PRIM_CAL_DICT = {
    "inc": emit_inc,
    "add1": emit_inc,
    "int->char": emit_int_char,
    "char->int": emit_char_int,
    "+": emit_add,
    "*": emit_mul,
}


def function(fh, fname, f):
    emit(fh, ".globl  %s" % fname)
    emit(fh, ".type   %s, @function" % fname)
    fh.write("%s:\n" % fname)
    fh.write(".LFB0:\n")
    emit(fh, ".cfi_startproc")

    emit_expr(fh, f)

    emit(fh, "ret")
    emit(fh, ".cfi_endproc")
    fh.write(".LFE0:\n")
    emit(fh, ".size   %s, .-%s" % (fname, fname))


def make_file(filename, expr):
    with open(filename, "w") as fh:
        file_preamble(fh)
        function(fh, "cref", expr)
        file_postamble(fh)

def is_immediate(x):
    if type(x) is int:
        return True
    if type(x) is str:
        return True
    return False


def is_call(x):
    return isinstance(x, (list, tuple))


def is_primcall(x):
    if not type(x[0]) is Symbol:
        return False
    sym = x[0].value()
    return sym in PRIM_CAL_DICT


def immediate_rep(x):
    if type(x) is int:
        return x << FIXNUM_SHIFT | FIXNUM_TAG

    if type(x) is bool:
        return (x << BOOL_SHIFT) | BOOL_TAG

    if type(x) is str:
        return (ord(x[0]) << CHAR_SHIFT) | CHAR_TAG

    assert False

def compile_program(fh, x):
    emit_expr(fh, x)
    emit(fh, "ret")
