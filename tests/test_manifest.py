import yaml

from tensixpe import Fabric, FpuPE, SfpuPE


def test_write_manifest(tmp_path):
    f = Fabric(mesh=(8, 8))
    fpu = f.place(FpuPE("FPU0", op="add"), coord=(0, 0))
    sfpu = f.place(SfpuPE("SFPU0", op="relu"), coord=(0, 1))
    Y = fpu(f.input("A"), f.input("B"))
    C = sfpu(Y)
    f.output("C", C)

    out = tmp_path / "manifest.yaml"
    f.to_manifest(out)
    assert out.exists()

    data = yaml.safe_load(out.read_text())
    for key in ("mesh", "pes", "streams", "inputs", "outputs"):
        assert key in data, f"missing key {key} in manifest"

    assert data["mesh"] == [8, 8]
    assert any(p["name"] == "FPU0" for p in data["pes"])
    assert any(p["name"] == "SFPU0" for p in data["pes"])
    assert "A" in data["inputs"] and "C" in data["outputs"]
