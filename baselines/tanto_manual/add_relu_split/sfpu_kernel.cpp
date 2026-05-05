// Manual Tanto baseline: SFPU stage C = relu(Y) (split mapping).

#include "tanto/all.h"

pipe<bfloat16> in_y;
pipe<bfloat16> out;
math<bfloat16> m;

void sfpu_kernel(uint32_t num_tiles) {
    for (uint32_t i = 0; i < num_tiles; ++i) {
        in_y.wait_front();
        out.reserve_back();

        m.copy(in_y, 0, 0);
        m.relu(0);
        m.pack(0, out);

        in_y.pop_front();
        out.push_back();
    }
}
