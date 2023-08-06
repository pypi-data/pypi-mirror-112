from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="yaml-validate",
    version="1.0.1",
    description="",
    long_description=readfile('README.md'),
    author="54696d21",
    author_email="void@example.com",
    url="https://github.com/54696d21/yaml-validate",
    py_modules=['yaml-validate'],
    license=readfile('LICENSE'),
    entry_points={'console_scripts': ['yaml-validate = main:main']},
)
