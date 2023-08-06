# skel

A quick skeleton generator for projects.

Fun fact: this project was generated using skel's `python-cli` template.

## Installation

### From Pip

Run `pip3 install skelgen`.

### From Source

Clone this repo.

Run `python3 setup.py install` to install globally.
Run `python3 setup.py install --user` to install for one user.


## Usage
Run `skel --help` for help.

Example usage:
Run `skel python-cli --path test` to generate a Python CLI application
in the `test` directory.

## Contributing

Got an idea for a template? Put in a merge request!
It's very easy to create a custom project template.
All file/folder names and contents are templated using
the Jinja2 template engine. All you need to do is write the templates,
add a ___template.py for configuration (see the Python template for
examples), and rebuild!

We also appreciate feature requests and bug reports.
