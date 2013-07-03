from setuptools import setup, find_packages
from reclass.version import __name__, __version__
setup(
    name = __name__,
    version = __version__,
    packages = find_packages(), 
    entry_points = {
      'console_scripts': ['reclass = reclass.main:run' ],
    },
    install_requires = ['pyyaml'],
    setup_requires = ['nose'],
)
