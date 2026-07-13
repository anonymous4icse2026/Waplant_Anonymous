(module
  (func (export "test") (result f32)
    block (result f32)
      f32.const 0 f32.const 0 f32.div
      i32.const 0 if (param f32) (result f32) end
    end
  )
)
