import sexpdata

# 1. return numbers
# 2. Math
# 3. logic
# 4. functions
# 5. FFI

#gcc -O0 -S -fomit-frame-pointer

#(define (fun1 x y)
# (+ x y))


def file_preamble():
#        .file   "two_func.c"
#        .text


def file_postamble():
#        .ident  "GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
#        .section        .note.GNU-stack,"",@progbits


def function():
#         .globl  func2
#         .type   func2, @function
# func2:
# .LFB0:
#         .cfi_startproc
#         movl    %edi, -4(%rsp)
#         movl    -4(%rsp), %eax
#         subl    $12, %eax
#         ret
#         .cfi_endproc
# .LFE0:
#         .size   func2, .-func2

def function_pre():
#         .globl  func2
#         .type   func2, @function
# func2:
# .LFB0:
#         .cfi_startproc

def function_end():
#         ret
#         .cfi_endproc
# .LFE0:
#         .size   func2, .-func2
