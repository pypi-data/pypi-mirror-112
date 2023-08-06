"""
Template configurations for additional questions etc.

All questions should have sensible defaults.
Questions without configured defaults will default to empty ('').

You can access data from plugins etc. by using
data[key]. Keys that do not exist will default to "".
"""
from pathlib import Path

def config(template_path: Path, project_path: Path, data: dict):
    questions = {
        "author": "Author (default: ''): ",
        "author_email": "Author Email (default: ''): ",
        "license": "License (default: 'MIT'): ",
        "description": "Short description (default: ''): ",
        "keywords": "Keywords? (default: ''): ",
        "project_url": f"Project URL? (default: '{data['git_remote']}'): ",
        "project_source": f"Project Source? (default: '{data['git_remote']}'): ",
    }

    defaults = {
        "license": "MIT",
        "description": "",
        "keywords": "",
        "project_url": data["git_remote"],
        "project_source": data["git_remote"]
    }

    return questions, defaults, data
