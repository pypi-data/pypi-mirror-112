from setuptools import setup

name = "types-pytest-lazy-fixture"
description = "Typing stubs for pytest-lazy-fixture"
long_description = '''
## Typing stubs for pytest-lazy-fixture

This is a PEP 561 type stub package for the `pytest-lazy-fixture` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pytest-lazy-fixture`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pytest-lazy-fixture. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `5e23e2c19a2b0fbbf6479d5e87223992f03cf84e`.
'''.lstrip()

setup(name=name,
      version="0.6.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pytest_lazyfixture-stubs'],
      package_data={'pytest_lazyfixture-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
