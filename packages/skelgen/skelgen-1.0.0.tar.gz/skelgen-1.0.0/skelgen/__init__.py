import sys
import argparse
from pathlib import Path

import skelgen.template
from skelgen.exception import TemplateNotExistsError

def main():
    templates = Path(__file__).parent / "templates"

    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="The template to scaffold with.")
    parser.add_argument("--name", help="The name of the project.")
    parser.add_argument("--overwrite", type=bool, help="Overwrite existing files.")
    parser.add_argument("--path",
                        default=Path.cwd(),
                        help="The path to the project.")

    args = parser.parse_args()

    if args.name is None:
        project_name = input("Name: ")
    else:
        project_name = args.name

    if not project_name:
        print("Project name cannot be empty.")
        sys.exit(1)

    template_folder = templates / args.template
    if not template_folder.exists():
        sys.tracebacklimit = 0
        raise TemplateNotExistsError("The specified template does not exist.")

    project_folder = Path(args.path)
    Path.mkdir(project_folder, parents=True, exist_ok=True)

    skelgen.template.fill_template(template_folder,
                                project_folder,
                                project_name=project_name,
                                overwrite=args.overwrite)
