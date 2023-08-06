from pathlib import Path
from skelgen.plugins.git import GitPlugin

def run_plugins(template_path: Path, project_path: Path):
    data = {}
    data.update(GitPlugin().get_data(project_path))
    return data
