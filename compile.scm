(define (compile-program x)
  (emit "movl $~a, %eax" x)
  (emit "ret"))


(define (compile-program x)
  (define (immediate-rep x)
    (cond
     ((integer? x) (shift x fixnum-shift))
     ; ...
     ))
  (emit "movl $~a, %eax" (immediate-rep x))
  (emit "ret"))

(define (emit-expr x)
  (cond
   ((immediate? x)
    (emit "movl $~a, %eax" (immediate-rep x)))
   ((primcall? x)
    (case (primcall-op x)
      ((add1)
       (emit-expr (primcall-operand1 x))
       (emit "addl $~a, %eax" (immediate-rep 1)))
					;...
      ))
   (else 
					; ...
    )))
