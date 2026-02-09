import sys
from pathlib import Path
submission_path = Path("/app/submission").resolve()
if submission_path not in [Path(p).resolve() for p in sys.path]:
    sys.path.insert(0, str(submission_path))
