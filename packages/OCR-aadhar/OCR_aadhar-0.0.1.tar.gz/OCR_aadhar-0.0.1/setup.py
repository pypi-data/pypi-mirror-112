import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'OCR_aadhar'
AUTHOR = 'ADARSH KISHORE MEHRA'
AUTHOR_EMAIL = 'adarsh.mehra800@gmail.com'
URL = 'https://github.com/adarsh1mehra/OCR-aadhar'

LICENSE = 'MIT License'
DESCRIPTION = 'Aadhar attributes Features recognition dataset with annotations.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
PACKAGES=['OCR_aadhar']
INSTALL_REQUIRES = []

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      include_package_data=True,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      package_data={'': ['OCR_aadhar/*.db']},
      )