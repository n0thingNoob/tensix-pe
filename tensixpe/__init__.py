"""TensixPE: CGRA-style PE graph abstraction over Tanto/TT-Metal."""

from tensixpe.ir.fabric import Fabric
from tensixpe.ir.pe import TensixPE, FpuPE, SfpuPE, FpuSfpuPE
from tensixpe.ir.stream import TileStream

__all__ = [
    "Fabric",
    "TensixPE",
    "FpuPE",
    "SfpuPE",
    "FpuSfpuPE",
    "TileStream",
]
