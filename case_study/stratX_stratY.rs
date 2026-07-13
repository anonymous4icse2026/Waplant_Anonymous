... ... ...

fn stratX(
    sig:   &Sig,
    dict:  &HashMap<Sig, Vec<DictInstr>>,
    mode:  BridgeMode,
    bias:  i32,
    stats: &StrategyStats,
) -> usize {
    fn is_scalar_numeric(t: &StackType) -> bool {
        matches!(
            t,
            StackType::I32 | StackType::I64 | StackType::F32 | StackType::F64
        )
    }

    fn is_numeric_type_change_sig(sig: &Sig) -> bool {
        sig.0.len() == 1
            && sig.1.len() == 1
            && is_scalar_numeric(&sig.0[0])
            && is_scalar_numeric(&sig.1[0])
            && sig.0[0] != sig.1[0]
    }

    fn is_numeric_constant_sig(sig: &Sig) -> bool {
        sig.0.is_empty()
            && sig.1.len() == 1
            && is_scalar_numeric(&sig.1[0])
    }

    fn is_numeric_arithmetic_or_identity_sig(sig: &Sig) -> bool {
        !sig.0.is_empty()
            && !sig.1.is_empty()
            && !sig_mentions_ref(sig)
            && !is_numeric_type_change_sig(sig)
    }

    let instrs = dict.get(sig);

    let has_static = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(di, DictInstr::Static(_)))
    });

    let has_struct_get = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(
            di,
            DictInstr::StructGetField { .. } | DictInstr::ArrayGetElem { .. }
        ))
    });

    let has_struct_new = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(di, DictInstr::StructNew { .. }))
    });

    let has_rebuild_struct = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(di, DictInstr::RebuildStruct { .. }))
    });

    let has_default_constructor = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(
            di,
            DictInstr::StructNewDefault(_)
                | DictInstr::ArrayNewDefault(_)
                | DictInstr::RefNull(_)
        ))
    });

    let has_ref_stash_set = sig.1.is_empty() && sig_mentions_ref(sig);

    let is_numeric_type_change = has_static && is_numeric_type_change_sig(sig);
    let is_numeric_constant    = has_static && is_numeric_constant_sig(sig);
    let is_numeric_arithmetic  = has_static && is_numeric_arithmetic_or_identity_sig(sig);

    let is_pure_synthesis = sig.0.is_empty() && !sig.1.is_empty();
    let is_pure_drop      = !sig.0.is_empty() && sig.1.is_empty();

    let mut reward: f64 = 0.50;

    // Main purpose of this strategy: prefer true numeric type-changing edges,
    // e.g. F64 -> I32, I32 -> F64, I64 -> F32.
    if is_numeric_type_change {
        reward += 0.80;
    }

    // Numeric constants are useful for rebuilding stacks, but should not be
    // considered equivalent to true conversion.
    if is_numeric_constant {
        reward += 0.25;
    }

    // Arithmetic/reduction is numeric and useful, but secondary.
    if is_numeric_arithmetic {
        reward += 0.20;
    }

    // Keep GC operations competitive so this strategy can still bridge mixed
    // numeric/GC contracts.
    if has_struct_get {
        reward += 0.45;
    }

    if has_struct_new {
        reward += 0.45;
    }

    if has_rebuild_struct {
        reward += 0.35;
    }

    if has_ref_stash_set {
        reward += if matches!(mode, BridgeMode::RefPreserving) {
            0.15
        } else {
            0.25
        };
    }

    if has_default_constructor {
        reward += 0.05;
    }

    // Mildly discourage pure synthesis/drop, but keep them available.
    if is_pure_synthesis {
        reward -= 0.10;
    }

    if is_pure_drop {
        reward -= 0.15;
    }

    reward_to_cost(reward, sig, bias, stats)
}

fn stratY(
    sig:   &Sig,
    dict:  &HashMap<Sig, Vec<DictInstr>>,
    mode:  BridgeMode,
    bias:  i32,
    stats: &StrategyStats,
) -> usize {
    fn is_scalar_numeric(t: &StackType) -> bool {
        matches!(
            t,
            StackType::I32 | StackType::I64 | StackType::F32 | StackType::F64
        )
    }

    fn is_numeric_type_change_sig(sig: &Sig) -> bool {
        sig.0.len() == 1
            && sig.1.len() == 1
            && is_scalar_numeric(&sig.0[0])
            && is_scalar_numeric(&sig.1[0])
            && sig.0[0] != sig.1[0]
    }

    fn is_numeric_constant_sig(sig: &Sig) -> bool {
        sig.0.is_empty()
            && sig.1.len() == 1
            && is_scalar_numeric(&sig.1[0])
    }

    fn is_numeric_reduction_or_arithmetic_sig(sig: &Sig) -> bool {
        !sig.0.is_empty()
            && !sig.1.is_empty()
            && !sig_mentions_ref(sig)
            && !is_numeric_type_change_sig(sig)
    }

    let instrs = dict.get(sig);

    let has_stash_set = instrs
        .is_some_and(|xs| xs.iter().any(|di| matches!(di, DictInstr::StashSet)));

    let has_stash_get = instrs
        .is_some_and(|xs| xs.iter().any(|di| matches!(di, DictInstr::StashGet)));

    let has_struct_get = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(
            di,
            DictInstr::StructGetField { .. } | DictInstr::ArrayGetElem { .. }
        ))
    });

    let has_struct_new = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(di, DictInstr::StructNew { .. }))
    });

    let has_rebuild_struct = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(di, DictInstr::RebuildStruct { .. }))
    });

    let has_default_constructor = instrs.is_some_and(|xs| {
        xs.iter().any(|di| matches!(
            di,
            DictInstr::StructNewDefault(_)
                | DictInstr::ArrayNewDefault(_)
                | DictInstr::RefNull(_)
        ))
    });

    let is_ref_stash = sig.1.is_empty() && sig_mentions_ref(sig);

    let is_numeric_type_change = is_numeric_type_change_sig(sig);
    let is_numeric_constant    = is_numeric_constant_sig(sig);
    let is_numeric_arithmetic  = is_numeric_reduction_or_arithmetic_sig(sig);

    // Tier 0: stack-reorder through locals.
    //
    // This is the desired path for type-swap behavior:
    //   [f64, i32] -> [i32, f64]
    // should prefer:
    //   local.set $i; local.set $f; local.get $i; local.get $f
    if has_stash_set || has_stash_get {
        return 1;
    }

    // Tier 1: GC structural operations. These are still meaningful
    // preservation/extraction operations, but should not beat simple stash
    // reorder when stash reorder is available.
    if has_struct_get || has_struct_new {
        return 10;
    }

    if has_rebuild_struct {
        return 15;
    }

    // Ref stash remains relatively cheap.
    if is_ref_stash {
        return if matches!(mode, BridgeMode::RefPreserving) {
            20
        } else {
            15
        };
    }

    // Tier 2: default constructors and ref.null. Synthesis-like, but sometimes
    // necessary for ref-domain targets such as externref.
    if has_default_constructor {
        return 100;
    }

    // Tier 3: generic fallback for neutral/static operations.
    let mut cost = 1_000usize;

    // Numeric arithmetic/reduction destroys values, so it should be much worse
    // than stash reorder.
    if is_numeric_arithmetic {
        cost = cost.max(10_000);
    }

    // Numeric constants rebuild the stack instead of swapping/reordering it.
    if is_numeric_constant {
        cost = cost.max(100_000);
    }

    // Numeric type-changing conversions are the main thing this strategy is
    // trying to avoid:
    //   [F64] -> [I32] via i32.trunc_f64_s
    //   [I32] -> [F64] via f64.convert_i32_s
    //   [I64] -> [F32] via f32.convert_i64_s
    if is_numeric_type_change {
        cost = cost.max(1_000_000);
    }

    // Keep bias/stats observable if your strategy infrastructure expects calls
    // to flow through reward_to_cost-like accounting. If not needed, this line
    // can be removed.
    let _ = (bias, stats);

    cost
}

... ... ...
