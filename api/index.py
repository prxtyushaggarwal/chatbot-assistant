import sys
from pathlib import Path

# Add root directory to path for imports
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from server import app
