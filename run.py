import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from calendar_app.app.main import main

if __name__ == "__main__":
    main()