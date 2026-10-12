"""Build the source and update GitHub Pages without deleting runtime documentation."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(["node", "scripts/verify-protected-runtime.mjs"], cwd=ROOT, check=True)
subprocess.run(["node", "node_modules/vite/bin/vite.js", "build"], cwd=ROOT, check=True)
subprocess.run(["python3", "tools/copy_assets.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "tools/validate.py"], cwd=ROOT, check=True)
shutil.copytree(ROOT / "dist", ROOT / "docs", dirs_exist_ok=True)
print("Updated docs/. Commit source changes and docs/ together to deploy.")
