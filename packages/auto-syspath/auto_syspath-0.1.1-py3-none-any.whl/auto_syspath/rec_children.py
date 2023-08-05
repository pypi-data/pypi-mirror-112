import sys
from pathlib import Path

for dir in set(path.parent for path in Path(".").glob("**/*.py")):
    sys.path.append(str(dir))