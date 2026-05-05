// Manual Tanto baseline: FPU stage Y = A + B (split mapping).

#include "tanto/all.h"

pipe<bfloat16> in0;
pipe<bfloat16> in1;
pipe<bfloat16> out_y;
math<bfloat16> m;

void fpu_kernel(uint32_t num_tiles) {
    for (uint32_t i = 0; i < num_tiles; ++i) {
        in0.wait_front();
        in1.wait_front();
        out_y.reserve_back();

        m.add(in0, in1, 0, 0, 0);
        m.pack(0, out_y);

        in0.pop_front();
        in1.pop_front();
        out_y.push_back();
    }
}
