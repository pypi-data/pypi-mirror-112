import setuptools
from skelgen.version import VERSION
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setuptools.setup(
    version=VERSION
)
