(module
  (memory 1)

  (func (export "main") (result i32)
    i32.const 0
    i32.load          ;; produces wait address 0

    i32.const 1       ;; expected value
    i64.const -1      ;; timeout

    memory.atomic.wait32
  )
)
