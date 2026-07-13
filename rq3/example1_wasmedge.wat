(module
  (type $point (struct (field i32)))
  (tag $e (param (ref null $point)))
  (func (export "main") (result i32)
    (local $exn exnref)
    block $h (result (ref null $point) exnref)
      try_table (catch_ref $e $h)
        ref.null $point
        throw $e
      end
      unreachable
    end
    local.set $exn
    drop
    block $h2 (result (ref null $point))
      try_table (catch $e $h2)
        local.get $exn
        throw_ref
      end
      unreachable
    end
    struct.get $point 0
  )
)