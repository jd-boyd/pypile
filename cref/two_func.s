	.file	"two_func.c"
	.text
	.globl	func2
	.type	func2, @function
func2:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	addl	%edx, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	func2, .-func2
	.globl	cref
	.type	cref, @function
cref:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$12, %esi
	movl	$51966, %edi
	call	func2
	subl	$559038737, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	cref, .-cref
	.ident	"GCC: (Ubuntu 4.9.1-16ubuntu6) 4.9.1"
	.section	.note.GNU-stack,"",@progbits
