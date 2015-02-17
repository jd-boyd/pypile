	.file	"return.c"
	.text
	.globl	cref
	.type	cref, @function
cref:
.LFB0:
	.cfi_startproc
	movl	$42, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	cref, .-cref
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
