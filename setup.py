from setuptools import setup, find_packages
setup(
    name = "Reclass",
    version = "1.0",
    packages = find_packages(), 
    entry_points = {
      'console_scripts': ['reclass = reclass.main:run' ],
    },
    install_requires = ['pyyaml'],
    setup_requires = ['nose'],
)
