from pathlib import Path
import importlib

test_path = Path("tests")

for file in test_path.glob("*.py"):
    if file.stem.startswith("_"):
        continue

    module = importlib.import_module(f"tests.{file.stem}")

    names = getattr(module, "__all__", None)
    if names is None:
        names = [n for n in vars(module) if not n.startswith("_")]

    for name in names:
        globals()[name] = getattr(module, name)
