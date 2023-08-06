"""
This is an example of a "shortcut" template.

It sort of cheats by using a separate generator.
We still have access to all the data from the plugins
and data system.
"""
import os
from shutil import which
from pathlib import Path
from skelgen.exception import UtilityNotExistsError

def config(template_path: Path, project_path: Path, data: dict):
    if which("npx") is None:
        raise UtilityNotExistsError(
            "This template requires the external npx utility, which is not installed on this system. Please install npx."
        )

    if project_path == Path.cwd():
        project_path = project_path / data["project_name"]

    if len(list(project_path.glob("**/*"))) == 0:
        os.rmdir(project_path)

    print(f"npx @vue/cli create {project_path}")
    os.system(f"npx @vue/cli create {project_path}")
    return {}, {}, data
