// Manual Tanto baseline: fused C = relu(A + B) on a single core.
// Hand-written skeleton — TODOs mark Ronin/Tanto API calls to wire up.

#include "tanto/host.h"

int main(int argc, char** argv) {
    // 1. Device + program
    // TODO: open_device(0); create_program(...);

    // 2. DRAM buffers
    // TODO: alloc_dram_buffer(buf_A); alloc_dram_buffer(buf_B); alloc_dram_buffer(buf_C);

    // 3. Pipes (in0, in1, out)
    // TODO: declare 3 bfloat16 32x32 pipes with buffering=2

    // 4. Place the fused kernel on a single core
    // TODO: place_kernel(program, "fused_kernel", coord=(0, 0));

    // 5. Runtime args + enqueue
    // TODO: set_runtime_args; enqueue_program(blocking=true);

    // 6. Read C back
    // TODO: read_buffer(buf_C, host_C);

    return 0;
}
