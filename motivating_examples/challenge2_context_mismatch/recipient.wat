(module
  (memory 1)

  (func (export "main") (result i32)
    i32.const 0
    i32.load          ;; produces address/value 0

    i32.const 1
    i64.const -1

    ;; Hole: [i32, i32, i64] -> [i32]
    i32.wrap_i64
    i32.add
    i32.add
  )
)
