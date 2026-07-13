(module
  (type (;0;) (func (result v128 v128 v128 v128 v128 v128 v128 v128 v128 v128)))
  (memory (;0;) 65536 65536)
  (export "main" (func 0))
  (export "memory" (memory 0))
  (func (;0;) (type 0) (result v128 v128 v128 v128 v128 v128 v128 v128 v128 v128)
    (local v128 v128 i32)
    v128.const i32x4 0xffffffff 0xffffffff 0xffffffff 0x00ffffff
    local.set 0
    local.get 0
    v128.const i32x4 0x0000b8ea 0x00000000 0x00000000 0x00000000
    i16x8.add_sat_s
    local.get 0
    v128.const i32x4 0x00591302 0x00000000 0x00000000 0x00000000
    f64x2.ne
    local.get 0
    v128.bitselect
    v128.any_true
    local.get 2
    i32.const 1
    i32.sub
    i32.const 4
    i32.mul
    i32.add
    memory.size
    i32.const 16
    i32.shl
    i32.const 0
    i32.sub
    i32.const 4
    i32.sub
    i32.const 1
    i32.or
    i32.rem_u
    i32.load
    i8x16.splat
    local.get 1
    local.get 1
    local.get 1
    i8x16.extract_lane_s 1
    v128.load8x8_s offset=3933 align=1
    v128.const i32x4 0x2b065bd7 0xdd6eeb92 0x2fd53550 0x0000c671
    i64x2.extmul_low_i32x4_s
    v128.const i32x4 0x00000000 0x00000000 0x00000000 0x00000000
    i16x8.q15mulr_sat_s
    local.get 0
    local.get 0
    i32.const 11
    local.get 0
    local.get 0
    i8x16.shuffle 15 9 5 5 3 1 6 14 14 13 8 4 13 1 6 13
    v128.load16_lane offset=9102 align=1 0
    i16x8.sub_sat_s
    i32.const 1091
    i8x16.shr_u
    i32.const 2382
    i16x8.shr_u
    i64x2.le_s
    local.get 0
    i32.const 2459
    i16x8.shl
    local.get 0
    v128.not
    v128.const i32x4 0x0000ce3e 0x00000000 0x00000000 0x00000000
    local.get 0
    local.get 0
    i8x16.le_s
    local.tee 0
    v128.const i32x4 0x89ec8ae1 0x0e7d47de 0x7c52a57e 0x0000ec0d
    i8x16.sub_sat_u
    local.tee 0
    f64x2.pmin
    local.tee 0
    v128.const i32x4 0x168b0961 0x9418e6de 0x638bc60b 0x00000018
    local.get 0
    i32x4.ge_s
    local.get 0
    v128.xor
    local.get 0
    local.get 0
    local.get 0
    i32.const 7769
    i32x4.replace_lane 0
    v128.const i32x4 0x00130f6d 0x00000000 0x00000000 0x00000000
    i8x16.add
    i32x4.mul
    local.get 0
    i32.const 3101
    i16x8.shr_s
    local.tee 0
    i32.const 1006
    i64x2.shl
    local.get 0
    local.get 0
    i32.const 2075
    i16x8.shl
    i32.const 1929
    i64x2.shr_u
    i16x8.extmul_high_i8x16_s
    v128.const i32x4 0x97a479da 0x000a66eb 0x00000000 0x00000000
    i32x4.min_u
    i16x8.q15mulr_sat_s
    f32x4.div
    i8x16.lt_u
    local.get 0
    local.get 0
    i32x4.max_u
    i16x8.min_u
    i64x2.lt_s
    i16x8.gt_u
    local.get 0
    v128.const i32x4 0x915eadc7 0x4f242cf3 0x5b3638a6 0x00000000
    i32x4.ne
    f32x4.ceil
    i32.const 3899
    i32x4.shr_u
    v128.const i32x4 0xdd72ae2a 0x00000000 0x00000000 0x00000000
    i32x4.lt_u
    local.get 0
    i64x2.extend_low_i32x4_u
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    local.get 0
    return
  )
  (data (;0;) (i32.const 1996866339) "")
)
