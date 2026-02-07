from setuptools import setup

setup(
    name="molsys_dev_tools",
    version="0.1.0",
    py_modules=["molsys_dev_setup"],
    entry_points={
        'console_scripts': [
            'molsys-dev-setup=molsys_dev_setup:main',
        ],
    },
)
