	.file	"stack_args.c"
	.text
	.globl	func8
	.type	func8, @function
func8:
.LFB0:
	.cfi_startproc
	movl	%edi, -4(%rsp)
	movl	%esi, -8(%rsp)
	movl	%edx, -12(%rsp)
	movl	%ecx, -16(%rsp)
	movl	%r8d, -20(%rsp)
	movl	%r9d, -24(%rsp)
	movl	-8(%rsp), %eax
	movl	-4(%rsp), %edx
	addl	%eax, %edx
	movl	-12(%rsp), %eax
	addl	%eax, %edx
	movl	-16(%rsp), %eax
	addl	%eax, %edx
	movl	-20(%rsp), %eax
	addl	%eax, %edx
	movl	-24(%rsp), %eax
	addl	%eax, %edx
	movl	8(%rsp), %eax
	addl	%eax, %edx
	movl	16(%rsp), %eax
	addl	%edx, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	func8, .-func8
	.globl	cref
	.type	cref, @function
cref:
.LFB1:
	.cfi_startproc
	subq	$16, %rsp
	.cfi_def_cfa_offset 24
	movl	$10, 8(%rsp)
	movl	$9, (%rsp)
	movl	$36, %r9d
	movl	$35, %r8d
	movl	$34, %ecx
	movl	$5, %edx
	movl	$12, %esi
	movl	$51966, %edi
	call	func8
	subl	$559038737, %eax
	addq	$16, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE1:
	.size	cref, .-cref
	.ident	"GCC: (Ubuntu/Linaro 4.8.1-10ubuntu9) 4.8.1"
	.section	.note.GNU-stack,"",@progbits
