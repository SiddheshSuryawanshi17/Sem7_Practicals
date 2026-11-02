"""Start Jupyter Notebook 6.x with a fix for newer tornado versions.

Newer tornado StaticFileHandler checks `self.allowed_symlink_directory`, which
notebook 6.x's FileFindHandler never sets -> every CSS/JS file gives HTTP 500
(blank page in the browser).
Usage:  python3 run_notebook.py Your_Notebook.ipynb
"""
import sys
from notebook.base.handlers import FileFindHandler

# FileFindHandler already restricts files to its own search roots.
FileFindHandler.allowed_symlink_directory = "/"

from notebook.notebookapp import main

sys.exit(main())
