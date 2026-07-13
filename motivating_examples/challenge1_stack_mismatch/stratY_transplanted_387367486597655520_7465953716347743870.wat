(module
  (type (;0;) (func (result i32)))
  (type (;1;) (func (param f64 f64 i32 f64 f32) (result i32)))
  (table (;0;) 2 funcref)
  (memory (;0;) 1)
  (global (;0;) (mut f64) f64.const -0x1.0035c4524daf8p+7 (;=-128.10501343916235;))
  (export "_main" (func 0))
  (export "memory" (memory 0))
  (elem (;0;) (i32.const 0) func 1 2)
  (func (;0;) (type 0) (result i32)
    (local i32 i64 f32 f64 f64 i32 f32 i64)
    i32.const 385
    f64.const 0x1.9cbe6f8f163aap+9 (;=825.4877795084515;)
    f64.store offset=39 align=2
    f64.const 0x1.4530cd2e8aa6bp+8 (;=325.1906308258537;)
    i32.const 702
    local.set 5
    local.set 4
    local.get 5
    local.get 4
    f64.const -0x1.d7441bb8030abp+712 (;=-39662775328485124000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000;)
    f64.abs
    f64.ge
    f32.const 0x1.c61bfp-69 (;=0.0000000000000000000030050422;)
    i32.const -1942415650
    i32.const 15652
    v128.const i32x4 0x05efb0f8 0x785ed6a5 0x63ec70af 0x84c9988e
    i32x4.bitmask
    local.set 5
    local.set 5
    local.set 5
    local.set 6
    local.set 5
    local.set 5
    local.get 4
    local.get 4
    local.get 7
    i64.const 11
    i64.eq
    select
    local.tee 3
    global.get 0
    i32.const 440
    i32.load16_u offset=58 align=1
    i32.const 178
    i32.load offset=16 align=2
    i32.and
    global.get 0
    f64.const 0x1.abf60cf2b5ea8p+8 (;=427.9611350721484;)
    i32.const 554
    f64.load offset=74 align=1
    local.tee 3
    local.get 3
    i64.reinterpret_f64
    i64.const 9218868437227405312
    i64.and
    i64.popcnt
    i64.const 11
    i64.eq
    select
    local.tee 3
    f64.min
    i32.const 758
    i32.load16_u offset=35 align=1
    i32.const 334
    i32.load16_s offset=81 align=1
    br_if 0
    drop
    f32.const 0x1.bbacd6p+9 (;=887.3503;)
    i32.const 1
    call_indirect (type 1)
  )
  (func (;1;) (type 0) (result i32)
    i32.const 0
  )
  (func (;2;) (type 1) (param f64 f64 i32 f64 f32) (result i32)
    (local i32 i64 f32 f64 i32 i32)
    i32.const 86
    local.set 10
    i32.const 684
    i32.load8_s offset=77
    local.tee 2
    i32.const 0
    call_indirect (type 0)
    i32.xor
    local.set 9
    loop ;; label = @1
      local.get 9
      i32.const 561
      i64.load offset=74 align=4
      i32.const 183
      i64.load offset=94 align=2
      i64.eq
      i32.add
      local.set 9
      local.get 10
      i32.const -1
      i32.add
      local.tee 10
      br_if 0 (;@1;)
    end
    local.get 9
    local.get 2
    i32.extend8_s
    i32.rotr
  )
)
