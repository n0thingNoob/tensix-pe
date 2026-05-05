# TensixPE design

TensixPE lifts a per-core Tanto/TT-Metal programming model into a
CGRA-style PE graph abstraction.

A `TensixPE` has:

- input/output tile-stream ports,
- local pipe / buffer resources,
- an internal compute template,
- a backend lowering rule (Tanto today; TT-Metal in the future).

## MVP PE types

- `FpuPE`     — matrix-engine elementwise (e.g. `add`)
- `SfpuPE`    — scalar/vector engine (e.g. `relu`)
- `FpuSfpuPE` — fused FPU then SFPU on the same core

## Two initial mappings for `C = relu(A + B)`

```text
Fused:
    [FpuSfpuPE]      # one core does both stages

Split:
    [FpuPE] -> [SfpuPE]  # two cores, dataflow over a pipe
```

## Lowering pipeline (current)

```text
Python IR (Fabric)
   │
   ├── manifest.yaml        (declarative graph)
   │
   └── Tanto backend
        ├── kernels/<pe>.cpp   (one per placed PE)
        ├── host.cpp           (device/program/buffers/pipes)
        ├── build.sh           (TODO: real Ronin build invocation)
        └── run_jitte.sh       (TODO: real Jitte run)
```

## Future PE types (deferred)

`ControlPE`, `RelayPE`, plus richer compute templates
(`matmul_gelu`, `block_sparse`) and an automatic-placement pass.
