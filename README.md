# Waplant — Artifact for Anonymous ICSE 2027 Submission

This repository is the supplementary artifact for a paper (currently under anonymous, double-blind
review at ICSE 2027) on **Waplant**, a code-transplantation technique for fuzzing production
WebAssembly (Wasm) runtimes. The prepared seed corpus `Bench2026` is attached in the following release 
tag: [Bench2026](https://github.com/anonymous4icse2026/Waplant_Anonymous/releases/tag/v0.0.1).

## What Waplant does

Waplant fuzzes a Wasm runtime by **transplantation**: it cuts a contiguous instruction range (a
"hole") out of a seed `.wasm` module and splices in a code fragment taken from a different
("donor") module, then runs the resulting hybrid module against the runtime under test. Two
problems arise at every splice point, and this artifact's motivating examples correspond to them
one-to-one:

1. **Stack-specification mismatch** (`motivating_examples/challenge1_stack_mismatch/`) — the donor
   fragment's required value-stack shape (its `prestack`/`poststack`, recorded per-hole as a
   `contract` in the metadata JSON) rarely matches what the recipient hole actually produces or
   expects. Waplant's **stack-bridging component (SBC)** selects instructions to reconcile the two
   stacks, and the paper compares two candidate strategies for doing so (see `case_study/` below).
2. **Module-context mismatch** (`motivating_examples/challenge2_context_mismatch/`) — a donor
   fragment can reference module-level constructs (memories, tables, types, globals, tags,
   `call_indirect` targets, …) that don't exist, or exist with incompatible attributes (e.g.
   shared vs. non-shared memory), in the recipient module. Waplant's **context reconciliation
   module (CRM)** rewrites/aligns these before the transplant, and it does so per construct kind:
   type definitions, variables, functions, memories, tables, `call_indirect` sites, and tags (this
   is directly evidenced by the per-construct ablations in `rq2/waplant_ablation.json`).

## Repository layout

```
.
├── motivating_examples/    # Two minimal examples of the transplantation problems above
├── case_study/             # Case study comparing the two SBC strategies (stratX/stratY)
├── rq1/                    # RQ1: bug-finding results and coverage progress comparison
├── rq2/                    # RQ2: ablation study (ties each bug/coverage gain to a component)
└── rq3/                    # RQ3: characterization of the bugs found (memory/functional, shallow/deep)
```

### `motivating_examples/`

- **`challenge1_stack_mismatch/`** — the same hole, cut from a seed and paired with a donor
  fragment, transplanted twice using two different stack-bridging strategies:
  - `donor_metadata_7465953716347743870.json`, `recipient_metadata_387367486597655520.json` — the
    hole/fragment/contract metadata for the donor and recipient (see [Metadata schema](#metadata-json-schema)).
  - `stratX_transplanted_387367486597655520_7465953716347743870.{wasm,wat}` and
    `stratY_transplanted_387367486597655520_7465953716347743870.{wasm,wat}` — the two resulting
    transplanted modules, in binary and text form.
  - `stratX_profile.txt`, `stratY_profile.txt` — line-coverage profiles (gcov-style, against the
    runtime's C source) captured while running each transplanted module, showing that the two
    bridging strategies drive execution through different internal runtime code paths.
- **`challenge2_context_mismatch/`** — a donor/recipient pair with a memory-attribute mismatch:
  - `donor.{wasm,wat}`, `recipient.{wasm,wat}` — the two source modules.
  - `no_mem_reconciled_trap.{wasm,wat}` — the transplant performed *without* context reconciliation:
    it traps at runtime. `trap_trace.txt` shows the resulting wasmtime trap, `atomic wait on
    non-shared memory`.
  - `mem_reconciled_no_trap.{wasm,wat}` — the same transplant *with* CRM's memory reconciliation
    applied: it runs cleanly.
  - `run_non_reconciled.sh` / `run_reconciled.sh` — one-line repro scripts, each invoking
    [wasmtime](https://wasmtime.dev/) directly:
    ```
    wasmtime run -W all-proposals=y -W shared-memory=y --invoke main <file>.wasm
    ```

### `case_study/`

An elaborate case study transplanting one hole (recipient id `3529427722592983174`, donor id
`6943238964362517065`; see `metadata_3529427722592983174.json` and
`metadata_6943238964362517065.json`) with each of the two competing SBC strategies:

- `stratX_seed1337_transplanted_3529427722592983174_6943238964362517065.{wasm,wat}`
- `stratY_seed1337_transplanted_3529427722592983174_6943238964362517065.{wasm,wat}`
- `stratX_stratY.rs` — an excerpt of the actual strategy implementations, included so the two
  approaches can be read side by side:
  - **`stratX`** scores each candidate bridging instruction with an additive `reward`, most
    strongly favoring genuine numeric type-conversion edges (e.g. `F64 -> I32`).
  - **`stratY`** instead assigns tiered integer `cost`s and strongly prefers reordering the stack
    through locals (`local.set`/`local.get`, referred to as "stash") over numeric
    type-converting instructions, which it treats as a last resort.

  This file is a documentation excerpt (it opens and closes with `... ... ...`) and is not meant
  to be compiled or run standalone. We have generated more bridging strategies using a Claude Code 
  agent loop with validation. We ran short campaigns with each LLM-generated bridging strategy function. 
  We manually evaluated whether each bridging strategy would generate diverse and unique bridge 
  sequences compared to other bridging strategies. We also manually evaluated whether the bridge sequence conforms to the desired developer objective e.g. (a) ... generate a bridging strategy function that ensures numeric conversions ... (b) ... generate a bridging strategy function that ensures type/value preservation through swapping existing types/values ... . Future work will scope out various bridge search strategy functions and empirically evaluate more strategies.

### `rq1/` — bug-finding and coverage (RQ1)

- **`bugs.tsv`** — every bug Waplant found, one per row: a `BugID` encoding the runtime and a short
  description, a link to the upstream issue, and its current `Status`. Summary:

  | Runtime  | Bugs found |
  |----------|-----------:|
  | Wasmer   | 10         |
  | WAMR     | 5          |
  | wasmi    | 2          |
  | WasmEdge | 2          |
  | wasm3    | 1          |
  | wazero   | 1          |
  | **Total**| **21**     |

  By status: 8 **fixed**, 10 **confirmed**, 11 **pending**. Two of
  the Wasmer rows (`wasmer_llvm_no-oob_A`/`_B`) were acknowledged together under a single upstream
  issue.

- **`coverage.json`** — branch coverage progress samples for four techniques (`Wasmaker`,
  `Wapplique`, `FreeWavm`, and `Waplant`), each against three runtimes (`wamr`, `wasmedge`,
  `wasmer`).
- **`plot_coverage.py`** — for RQ1 coverage progress figure (one panel per runtime)
  from `coverage.json`:
  ```
  python3 rq1/plot_coverage.py rq1/coverage.json -o coverage_3panel
  ```
  Writes `coverage_3panel.png` and `.pdf`.

### `rq2/` — ablation study (RQ2)

- **`waplant_ablation.json`** — mean coverage samples for full Waplant (`waplant`) and eleven
  ablations, each disabling one component: `waplant_no_crm`, `waplant_no_sbc` (whole-component
  ablations); `crm_no_typedefs`, `crm_no_variables`, `crm_no_functions`, `crm_no_memories`,
  `crm_no_tables`, `crm_no_callindirect`, `crm_no_tags` (per-construct CRM ablations); and
  `sbc_no_stratX`, `sbc_no_stratY` (per-strategy SBC ablations).
- **`analyze.py`** — for each ablation and runtime, computes the mean coverage drop versus the
  `waplant` baseline, a one-sided Mann–Whitney U test, and Cliff's delta effect size:
  ```
  cd rq2 && python3 analyze.py
  ```
  Requires `numpy` and `scipy` (reads `waplant_ablation.json` via a path relative to `rq2/`).

### `rq3/` — bug characterization (RQ3)

- **`characterization.txt`** — buckets every bug from `rq1/bugs.tsv` along two axes: **Memory**
  vs. **Functional** (crash class), and **Shallow** vs. **Deep** (how much runtime-internal state
  the triggering input had to satisfy to reach the bug).
- **`example1_wasmedge.{wasm,wat}`**, **`example2_wasmer.{wasm,wat}`** — two concrete
  bug-triggering inputs, given in both binary and human-readable text form.

## Metadata JSON schema

`metadata_*.json`, `donor_metadata_*.json`, and `recipient_metadata_*.json` files (in
`case_study/` and `motivating_examples/challenge1_stack_mismatch/`) share one schema:

| Field | Meaning |
|---|---|
| `id` | Numeric id, also embedded in the paired `.wasm`/`.wat` filenames |
| `original` | The source seed file this hole/fragment was cut from |
| `hole.func_idx`, `hole.instr_range` | Which function and instruction range was cut out |
| `hole.hole_ctx` | In-scope types/locals/globals/calls/memories/tables/tags at the splice point |
| `hole.enclosing_labels` | Structured-control-flow labels (e.g. blocks) enclosing the hole |
| `contract.prestack` / `contract.poststack` | Value-stack types the splice must produce/consume |
| `fragment` | The donor code being spliced in, with its own context and any external branches |

Files are cross-referenced by matching the numeric `id` embedded in their filenames — e.g.
`stratX_seed1337_transplanted_3529427722592983174_6943238964362517065.wasm` transplants recipient
id `3529427722592983174` with donor id `6943238964362517065`.

## Commands to generate the figures/tables

| Result | Command | Requires |
|---|---|---|
| RQ1 coverage plot | `python3 rq1/plot_coverage.py rq1/coverage.json -o coverage_3panel` | `numpy`, `matplotlib` |
| RQ2 ablation table | `cd rq2 && python3 analyze.py` | `numpy`, `scipy` |
| Motivating example 2 (traps) | `cd motivating_examples/challenge2_context_mismatch && sh run_non_reconciled.sh` then `sh run_reconciled.sh` | [wasmtime](https://wasmtime.dev/) CLI on `PATH` |

```
pip install numpy scipy matplotlib
```

`.wat` text-format twins are provided next to almost every `.wasm` binary in this repository, so
inspecting a module rarely requires a disassembler. Where only a `.wasm` is present, any
standard Wasm disassembler (e.g. `wasm2wat` from [WABT](https://github.com/WebAssembly/wabt), or
`wasm-tools print`) can be used to inspect it.
