	.file	"math_add.c"
	.text
	.globl	cref
	.type	cref, @function
cref:
.LFB0:
	.cfi_startproc
	movl	$5, -8(%rsp)
	movl	$-559038737, -4(%rsp)
	movl	-4(%rsp), %eax
	movl	-8(%rsp), %edx
	addl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	cref, .-cref
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
