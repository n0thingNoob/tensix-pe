# Tanto manual baselines

Hand-written Tanto skeletons for `C = relu(A + B)`. **Not generated.**

These mirror the two example mappings under `examples/` and are the human
reference the codegen will eventually be measured against.

- `tanto_manual/add_relu_fused/` — single-kernel fused (FpuSfpuPE analog)
- `tanto_manual/add_relu_split/` — two-kernel split (FpuPE → SfpuPE analog)

Like the generated outputs, these are **skeletons** with TODO markers; they
are not expected to compile against Ronin in the MVP.
