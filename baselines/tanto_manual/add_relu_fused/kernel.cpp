// Manual Tanto baseline: fused kernel for C = relu(A + B).
// Single core does both FPU add and SFPU relu before packing.

#include "tanto/all.h"

pipe<bfloat16> in0;
pipe<bfloat16> in1;
pipe<bfloat16> out;
math<bfloat16> m;

void fused_kernel(uint32_t num_tiles) {
    for (uint32_t i = 0; i < num_tiles; ++i) {
        in0.wait_front();
        in1.wait_front();
        out.reserve_back();

        m.add(in0, in1, 0, 0, 0);
        m.relu(0);
        m.pack(0, out);

        in0.pop_front();
        in1.pop_front();
        out.push_back();
    }
}
