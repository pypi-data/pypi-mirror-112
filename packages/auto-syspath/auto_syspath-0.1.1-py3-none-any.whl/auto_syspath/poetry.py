import sys
from pathlib import Path
import inspect

stack = inspect.stack()
for s in stack[1:]:
    m = inspect.getmodule(s[0])
    if m:
        current = Path(m.__file__).parent
        break

for _ in range(3):
    entries = list(str(entry.name) for entry in current.iterdir())
    if "poetry.toml" in entries:
        sys.path.append(str(current))
        break
    current = current.parent