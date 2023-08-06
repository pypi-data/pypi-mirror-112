from setuptools import setup

name = "types-polib"
description = "Typing stubs for polib"
long_description = '''
## Typing stubs for polib

This is a PEP 561 type stub package for the `polib` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `polib`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/polib. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9d5046ee7f4fad0f60bbdd807e46da9c22a2f9e0`.
'''.lstrip()

setup(name=name,
      version="1.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['polib-stubs'],
      package_data={'polib-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
