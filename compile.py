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


def emit_funcall(fh, l):
    print ("EFun")
    {
        "inc": emit_inc,
        "add": emit_add_const
    }[l[0].tosexp()](fh, l[1:])


def emit_expr(fh, e):
    print("EEx:", repr(e))
    if isinstance(e, int):
        emit_int(fh, e)
        return
    if isinstance(e, (list, tuple)):
        emit_funcall(fh, e)
        return
    assert False, "Couldn't figure out what to emit"


def emit_inc(fh, l):
    print ("ea1")
    emit_int(fh, l[0])
    fh.write("        addl $1, %eax\n")


def emit_add_const(fh, l):
    emit_int(fh, l[0])
    fh.write("        addl $%d, %%eax\n" % l[1])
    

def emit_int(fh, c):
    fh.write("        mov $%d, %%eax\n" % c)


def function(fh, fname, f):
    function_pre(fh, fname)
    emit_expr(fh, f)
    function_end(fh, fname)


def function_pre(fh, fname):
    fh.write("        .globl  %s\n" % fname)
    fh.write("        .type   %s, @function\n" % fname)
    fh.write("%s:\n" % fname)
    fh.write(".LFB0:\n")
    fh.write("        .cfi_startproc\n")


def function_end(fh, fname):
    fh.write("        ret\n")
    fh.write("        .cfi_endproc\n")
    fh.write(".LFE0:\n")
    fh.write("        .size   %s, .-%s\n" % (fname, fname))


def make_file(filename, expr):
    with open(filename, "w") as fh:
        file_preamble(fh)
        function(fh, "cref", expr)
        file_postamble(fh)

def load_file(file_str):
    file_fcns = ScmFile()
    statements = sexpdata.parse(file_str)
    
    for statement in statements:
        if statement[0] != Symbol("define"):
            assert False, "Only define statements handled"
        proto = statement[1]
        file_fcns.add(proto[0].tosexp(), proto[1:], statement[2:])
    return file_fcns

class ScmFile:
    def __init__(self):
        self.functions = {}

    def add(self, name, args, fcn):
        if len(args) > 6:
            assert False, "6 max args"
        self.functions[name] = (args, fcn)
