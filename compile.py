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

label_count = 0
def unique_label():
    lbl = "L_%d" % label_count
    label_count += 1
    return lbl


def emit(fh, instruction):
    fh.write("        " + instruction + "\n")
        

def emit_expr(fh, x, si, env):
    print("emit_expr:", repr(x))
    if is_immediate(x):
        emit(fh, "mov ${0}, %eax".format(immediate_rep(x)))
        return

    if is_var(x, env):
        emit_var(fh, x, si, env)
        return

    if is_primcall(x):
        PRIM_CALL_DICT[x[0].tosexp()](fh, x[1:], si, env)
        return

    if is_let(x):
        emit_let(fh, x[1], x[2], si, env)
        return

        
    assert False, "Couldn't figure out what to emit"


def emit_var(fh, x, si, env):
    name = x.value()
    print("n", name)
    emit(fh, "movq {0}(%rsp), %rax".format(env[name]))

def emit_let(fh, bindings, body, si, env):
    print("let", bindings, body, si, env)
    if not len(bindings):
        emit_expr(fh, body, si, env)
        return
    #do something
    bind = bindings[0]
    bind_name = bind[0].value()
    emit_expr(fh, bind[1], si, env)
    emit(fh, "movq %rax, {0}(%rsp)".format(si))
    env[bind_name] = si
    emit_let(fh, bindings[1:], body, si-8, env)


def emit_mul(fh, x, si, env):
    assert len(x) == 2
    print("emit add")
    emit_expr(fh, x[1], si, env)
    emit(fh, "movq %rax, {0}(%rsp)".format(si))
    emit_expr(fh, x[0], si-8, env)
    emit(fh, "imulq   {0}(%rsp), %rax".format(si))
    emit(fh, "sarl $2, %eax")
 

def emit_add(fh, x, si, env):
    assert len(x) == 2
    print("emit add")
    emit_expr(fh, x[1], si, env)
    emit(fh, "movq %rax, {0}(%rsp)".format(si))
    emit_expr(fh, x[0], si-8, env)
    emit(fh, "addq   {0}(%rsp), %rax".format(si))


def emit_null(x, si):
    pass


def emit_zero(x, si):
    pass


def emit_int_char(fh, x, si, env):
    emit_expr(fh, x[0], si, env)
    emit(fh, "sall $6, %eax")
    emit(fh, "orl $15, %eax")


def emit_char_int(fh, x, si, env):
    print("emit_char_int(", x, ")")
    emit_expr(fh, x[0], si, env)
    emit(fh, "sarl $8, %eax")
    emit(fh, "sall $2, %eax")


def emit_inc(fh, l, si, env):
    print("emit_inc")
    emit_expr(fh, l[0], si, env)
    emit(fh, "addl ${0}, %eax".format(immediate_rep(1)))



 
PRIM_CALL_DICT = {
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

    emit_expr(fh, f, -8, {})

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
    return sym in PRIM_CALL_DICT


def is_var(x, env):
    print("iv", x)
    if not type(x) is Symbol:
        return False
    return x.value() in env


def is_let(x):
    print("il", x)
    if not type(x[0]) is Symbol:
        return False
    return x[0].value() == "let"


def immediate_rep(x):
    if type(x) is int:
        return x << FIXNUM_SHIFT | FIXNUM_TAG

    if type(x) is bool:
        return (x << BOOL_SHIFT) | BOOL_TAG

    if type(x) is str:
        return (ord(x[0]) << CHAR_SHIFT) | CHAR_TAG

    assert False

def compile_program(fh, x):
    emit_expr(fh, x, -8)
    emit(fh, "ret")
