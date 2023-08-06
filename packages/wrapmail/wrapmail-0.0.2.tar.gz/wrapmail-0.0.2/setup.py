from setuptools import setup, find_packages
import codecs
import os
import pathlib
import pkg_resources

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'A package that helps to send emails through Python utilizing an OOP logic'
LONG_DESCRIPTION = 'A package that helps to send emails through Python utilizing an OOP logic. Includes a wrapper for Gmail API and an SMTP-based system'

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# Setting up
setup(
    name="wrapmail",
    version=VERSION,
    author="Alperen Yıldız",
    author_email="<alperenyildiz@sabanciuniv.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'mail','gmail','api','smtp'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)