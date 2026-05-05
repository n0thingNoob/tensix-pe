# tensix-pe

A research prototype for **TensixPE**: a CGRA-style Processing-Element graph
abstraction that lifts the per-core Tenstorrent / Tanto programming model
into a higher-level dataflow IR.

## What is TensixPE?

A `Fabric` of placed `TensixPE` nodes (`FpuPE`, `SfpuPE`, `FpuSfpuPE`)
connected by `TileStream`s. The user writes a small Python graph; a backend
lowers it to per-core Tanto kernels + a host program.

## What this is *not*

This is **not** Ronin/Tanto itself — Tanto is a per-core C++ kernel DSL.
TensixPE sits *above* Tanto and emits Tanto code as one of several possible
backends.

## Why Tanto first?

Tanto already provides high-level primitives (`pipe`, `math`, semaphores)
and runs through the **Jitte** functional emulator, which lets us debug the
generated dataflow before touching real hardware.

## MVP scope

- Python IR: `Fabric`, `TensixPE` family, `TileStream`
- Tanto codegen backend (skeleton C++ + scripts; not yet built/run)
- Two generated examples: `add_relu_fused`, `add_relu_split`
- Two hand-written Tanto baselines mirroring the examples
- Experiment runner that validates file layout

Currently supported example: **`C = relu(A + B)`**.

- Fused mapping: `[FpuSfpuPE]`
- Split mapping: `[FpuPE] -> [SfpuPE]`

## Ronin submodule

Ronin (which contains Tanto + Jitte) is consumed only as a git submodule at
`external/ronin/`. It is **never** vendor-copied or modified in this repo.

```bash
# preferred (your fork)
./scripts/setup_ronin.sh git@github.com:<your-username>/ronin.git

# upstream fallback
git submodule add git@github.com:tenstorrent/ronin.git external/ronin
git submodule update --init --recursive
```

If `external/ronin` is already present, `./scripts/setup_ronin.sh` (no args)
just runs `git submodule update --init --recursive`.

## How to run

```bash
pip install pyyaml jinja2 pytest    # only if missing

python examples/add_relu_fused_pe.py
python examples/add_relu_split_pe.py
python experiments/add_relu/run_all.py
pytest -q
```

The example scripts emit to `generated/tanto/<name>/`; `run_all.py` checks
that all expected files exist and that the manual baselines are present.

## Baselines

Hand-written Tanto skeletons live under `baselines/tanto_manual/`. They are
intentionally not generated — they're the human reference the codegen will
eventually be measured against.

## Out of scope (deferred)

- Compiling real Tanto code
- Running real Jitte
- TT-Metal backend (placeholder doc only)
- Hardware performance claims
- `ControlPE`, `RelayPE`
- `matmul_gelu`, `block_sparse`
- Automatic placement
