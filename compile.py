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


FIXNUM_MASK = 3
FIXNUM_TAG = 0
FIXNUM_SHIFT = 2

def emit(fh, instruction):
    fh.write("        " + instruction + "\n")
        

def emit_funcall(fh, l):
    print("emit_funcall")
    {
        "inc": emit_inc,
        "add": emit_add_const
    }[l[0].tosexp()](fh, l[1:])


def emit_expr(fh, x):
    print("emit_expr:", repr(x))
    if is_immediate(x):
        emit(fh, "mov ${0}, %eax".format(immediate_rep(x)))
        return
    if not is_call(x):
        assert False, "If not primitive, must be call."

    if is_primcall(x):
        {
            "inc": emit_inc,
            "add1": emit_inc
        }[x[0].tosexp()](fh, x[1:])
        return
 
    assert False, "Couldn't figure out what to emit"

def emit_inc(fh, l):
    print("emit_inc")
    emit_expr(fh, l[0])
    emit(fh, "addl ${0}, %eax".format(immediate_rep(1)))


def emit_add_const(fh, l):
    emit_expr(fh, l[0])
    emit(fh, "addl ${0}, %eax".format(immediate_rep(l[1])))
  

def function(fh, fname, f):
    function_pre(fh, fname)
    emit_expr(fh, f)
    emit(fh, "ret")
    function_end(fh, fname)

def function_pre(fh, fname):
    emit(fh, ".globl  %s" % fname)
    emit(fh, ".type   %s, @function" % fname)
    fh.write("%s:\n" % fname)
    fh.write(".LFB0:\n")
    emit(fh, ".cfi_startproc")


def function_end(fh, fname):
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
    return False


def is_call(x):
    return isinstance(x, (list, tuple))


def is_primcall(x):
    if not type(x[0]) is Symbol:
        return False
    sym = x[0].value()
    return sym in ['add1', 'inc']


def immediate_rep(x):
    if type(x) is int:
        return x << FIXNUM_SHIFT
    assert False

def compile_program(fh, x):
    emit_expr(fh, x)
    emit(fh, "ret")
