	.file	"two_func.c"
	.text
	.globl	func2
	.type	func2, @function
func2:
.LFB0:
	.cfi_startproc
	movl	%edi, -4(%rsp)
	movl	%esi, -8(%rsp)
	movl	-8(%rsp), %eax
	movl	-4(%rsp), %edx
	subl	%eax, %edx
	movl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	func2, .-func2
	.globl	cref
	.type	cref, @function
cref:
.LFB1:
	.cfi_startproc
	movl	$12, %esi
	movl	$51966, %edi
	call	func2
	subl	$559038737, %eax
	ret
	.cfi_endproc
.LFE1:
	.size	cref, .-cref
	.ident	"GCC: (Ubuntu/Linaro 4.8.1-10ubuntu9) 4.8.1"
	.section	.note.GNU-stack,"",@progbits
