(module
  (memory 1 1 shared)

  (func (export "main") (result i32)
    i32.const 0       ;; address
    i32.const 1       ;; expected value
    i64.const -1      ;; infinite timeout

    ;; Fragment: [i32, i32, i64] -> [i32]
    memory.atomic.wait32
  )
)
