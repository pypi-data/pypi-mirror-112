from setuptools import setup

name = "types-aiofiles"
description = "Typing stubs for aiofiles"
long_description = '''
## Typing stubs for aiofiles

This is a PEP 561 type stub package for the `aiofiles` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `aiofiles`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/aiofiles. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `42247feefb58f59925848b5c70c864afeda37fac`.
'''.lstrip()

setup(name=name,
      version="0.1.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['aiofiles-stubs'],
      package_data={'aiofiles-stubs': ['os.pyi', 'base.pyi', '__init__.pyi', 'threadpool/text.pyi', 'threadpool/__init__.pyi', 'threadpool/binary.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
