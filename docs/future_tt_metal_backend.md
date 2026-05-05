# Future: TT-Metal backend

Placeholder. Not implemented in the MVP.

Planned scope:

- Lower the TensixPE IR directly to TT-Metal host + kernels
  (bypassing Tanto, for fairer hardware-perf attribution).
- Run on real Wormhole devices and collect device-profiler timelines.
- Compare generated TT-Metal against a hand-written TT-Metal baseline
  for the same `C = relu(A + B)` graph (fused vs. split).
- Use the comparison to study fuse-vs-split tradeoffs (latency,
  throughput, L1 pressure) at the PE granularity.

Until then the Tanto backend (with Jitte for functional checks) is the
only end-to-end path.
