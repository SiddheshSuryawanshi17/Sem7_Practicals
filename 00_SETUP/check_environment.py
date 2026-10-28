# Run this FIRST on the lab PC:   python 00_SETUP/check_environment.py
# Tells you what is installed and what to install for each subject.
import importlib
import shutil
import subprocess
import sys

print(f"Python {sys.version.split()[0]}  ({sys.executable})\n")

checks = [
    ("numpy", "ML"), ("pandas", "ML"), ("matplotlib", "ML"), ("seaborn", "ML"),
    ("sklearn", "ML"), ("scipy", "ML (A6 dendrogram)"), ("tensorflow", "ML A3 (optional - sklearn fallback exists)"),
    ("notebook", "ML (jupyter notebook)"), ("PIL", "CSDF A2 CAPTCHA image (optional - text fallback)"),
    ("selenium", "STQA UI test (optional)"),
]
missing = []
for mod, use in checks:
    try:
        m = importlib.import_module(mod)
        print(f"  [OK]      {mod:<12} {getattr(m, '__version__', ''):<10} {use}")
    except Exception:
        print(f"  [MISSING] {mod:<12} {'':<10} {use}")
        missing.append({"sklearn": "scikit-learn", "PIL": "pillow"}.get(mod, mod))

print()
for tool, use in [("g++", "DAA C++ programs"), ("java", "optional")]:
    path = shutil.which(tool)
    print(f"  [{'OK' if path else 'MISSING':<7}] {tool:<12} {use}")

if missing:
    print("\nInstall missing packages with:")
    print(f"  {sys.executable} -m pip install " + " ".join(missing))
else:
    print("\nEverything is installed. You are good to go!")

if shutil.which("g++"):
    out = subprocess.run(["g++", "--version"], capture_output=True, text=True).stdout.splitlines()
    print("\n" + (out[0] if out else ""))
