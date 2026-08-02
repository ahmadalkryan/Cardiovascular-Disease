# path_setup.py - إعداد مسار المشروع

import sys
import os

def setup_path():
   
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root


PROJECT_ROOT = setup_path()