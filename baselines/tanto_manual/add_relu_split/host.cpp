// Manual Tanto baseline: split Y = A + B; C = relu(Y) across two cores.
// Hand-written skeleton — TODOs mark Ronin/Tanto API calls to wire up.

#include "tanto/host.h"

int main(int argc, char** argv) {
    // 1. Device + program
    // TODO: open_device(0); create_program(...);

    // 2. DRAM buffers (A, B, C). Y stays on-chip via a pipe.
    // TODO: alloc_dram_buffer(buf_A); alloc_dram_buffer(buf_B); alloc_dram_buffer(buf_C);

    // 3. Pipes:
    //    - input pipes for A, B feeding FPU core
    //    - intermediate pipe Y between FPU and SFPU cores
    //    - output pipe out of SFPU core
    // TODO: declare 4 bfloat16 32x32 pipes with buffering=2

    // 4. Place kernels:
    //    fpu_kernel  at (0, 0)  -- consumes A, B; produces Y
    //    sfpu_kernel at (0, 1)  -- consumes Y; produces C
    // TODO: place_kernel(program, "fpu_kernel", coord=(0, 0));
    // TODO: place_kernel(program, "sfpu_kernel", coord=(0, 1));

    // 5. Runtime args + enqueue
    // TODO: set_runtime_args; enqueue_program(blocking=true);

    // 6. Read C back
    // TODO: read_buffer(buf_C, host_C);

    return 0;
}
