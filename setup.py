#!/usr/bin/env python
# Stupid shit happened in pip 10: https://stackoverflow.com/a/49867265/965332
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

requirements = parse_requirements("./requirements.txt", session=False)

setup(name='organizadorImagenes',
      version="0.2",
      description='Aplicacion para organizar imagenes en un directorio',
      long_description=readme,
      long_description_content_type="text/markdown",
      author='Valdr Stiglitz',
      author_email='valdr.stiglitz@gmail.com',
      url='https://github.com/ValdrST/vOrganizadorImagenes',
      packages=set(['vOrganizadorImagenes', 'vOrganizadorImagenes.tools']),
      include_package_data=True,
      install_requires=[str(requirement.req) for requirement in requirements],
      entry_points={
          'console_scripts': ['vOrganizadorImagenes = vOrganizadorImagenes:main']
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          "Operating System :: OS Independent",
      ])
