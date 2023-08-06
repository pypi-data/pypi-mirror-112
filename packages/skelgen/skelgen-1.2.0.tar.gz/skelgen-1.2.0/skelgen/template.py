import sys
import importlib
import mimetypes
from collections import defaultdict
from pathlib import Path
import jinja2

import skelgen.plugins

def run_config(template_path: Path, project_path: Path, data: dict):
    """
    Ask additional questions in a template.
    Template-specific questions are contained in
    ${template_path}/___questions.py (3 underscores).
    """

    sys.path.append(str(template_path))
    try:
        template = importlib.import_module("___template")
    except ModuleNotFoundError:
        # No additional questions
        return data

    questions, defaults, data = template.config(template_path, project_path, data)

    for var, question in questions.items():
        data[var] = input(question)
        if data[var] == "":
            data[var] = defaults.get(var, "")

    return data

def fill_template(template_path: Path, project_path: Path, **kwargs):
    data = {
        "template_path": template_path,
        "project_path": project_path,
        **kwargs,
        **skelgen.plugins.run_plugins(template_path, project_path)
    }
    data = run_config(template_path, project_path, defaultdict(str, data))

    print("Scaffolding...")

    for path in template_path.glob("**/*"):
        rel_path = path.relative_to(template_path)
        path_templated = jinja2.Template(str(rel_path)).render(data)
        if path_templated.endswith(".___tmpl"):
            path_templated = path_templated.split(".___tmpl")[0]

        if Path(path_templated).name.startswith("___"):
            # Skip files prefixed with ___ (e.g. template config)
            continue

        if path.is_dir():
            Path.mkdir(project_path / path_templated, parents=True, exist_ok=True)
            print("Copied", project_path / path_templated)
        else:
            try:
                with open(path, "r") as content:
                    template = jinja2.Template(content.read())

                if data["overwrite"] or not (project_path / path_templated).exists():
                    with open(str(project_path / path_templated), "w") as out:
                        out.write(template.render(data))
                    print("Copied", project_path / path_templated)
                else:
                    print(f"File {project_path / path_templated} exists, skipping")
            except UnicodeDecodeError:
                # File is not text, should not be templated
                pass

    print("---")
    print("Done!")
