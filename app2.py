# app.py is an alias to app2.py for standard streamlit execution
import runpy
import sys
from pathlib import Path

app2_path = Path(__file__).parent / "app2.py"
runpy.run_path(str(app2_path), run_name="__main__")
