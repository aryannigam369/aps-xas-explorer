"""Run after a Data app build to include original download assets."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
shutil.copytree(root/'public/raw',root/'dist/raw',dirs_exist_ok=True)
shutil.copy2(root/'public/raw-data.zip',root/'dist/raw-data.zip')
(root/'dist/.nojekyll').touch()
print('Original source downloads copied into dist/.')
