from tensixpe import Fabric, FpuPE, SfpuPE, FpuSfpuPE, TileStream


def test_fabric_input_output():
    f = Fabric(mesh=(8, 8))
    A = f.input("A")
    assert isinstance(A, TileStream)
    assert "A" in f.inputs

    pe = f.place(FpuSfpuPE("PE0"), coord=(0, 0))
    C = pe(A, f.input("B"))
    f.output("C", C)

    assert "C" in f.outputs
    assert f.outputs["C"].name == "PE0_out0"


def test_fpu_pe_call_returns_stream():
    f = Fabric(mesh=(8, 8))
    fpu = f.place(FpuPE("FPU0", op="add"), coord=(0, 0))
    out = fpu(f.input("A"), f.input("B"))
    assert isinstance(out, TileStream)
    assert out.name == "FPU0_out0"
    assert out.src is fpu


def test_sfpu_pe_call_returns_stream():
    f = Fabric(mesh=(8, 8))
    sfpu = f.place(SfpuPE("SFPU0", op="relu"), coord=(0, 1))
    out = sfpu(f.input("X"))
    assert isinstance(out, TileStream)
    assert out.name == "SFPU0_out0"


def test_fpu_sfpu_pe_call_returns_stream():
    f = Fabric(mesh=(8, 8))
    pe = f.place(FpuSfpuPE("PE0"), coord=(0, 0))
    out = pe(f.input("A"), f.input("B"))
    assert isinstance(out, TileStream)
    assert out.name == "PE0_out0"


def test_manifest_dict_has_pe_and_streams():
    f = Fabric(mesh=(8, 8))
    pe = f.place(FpuSfpuPE("PE0", fpu_op="add", sfpu_op="relu"), coord=(0, 0))
    C = pe(f.input("A"), f.input("B"))
    f.output("C", C)

    md = f.to_manifest_dict()
    assert md["mesh"] == [8, 8]
    assert any(p["name"] == "PE0" and p["type"] == "FpuSfpuPE" for p in md["pes"])
    stream_names = {s["name"] for s in md["streams"]}
    assert {"A", "B", "PE0_out0"} <= stream_names
