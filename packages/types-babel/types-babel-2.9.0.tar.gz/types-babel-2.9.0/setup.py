from setuptools import setup

name = "types-babel"
description = "Typing stubs for babel"
long_description = '''
## Typing stubs for babel

This is a PEP 561 type stub package for the `babel` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `babel`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/babel. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `607aa37ee9a5c380baedb4938148fb3280f833e3`.
'''.lstrip()

setup(name=name,
      version="2.9.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['babel-stubs'],
      package_data={'babel-stubs': ['numbers.pyi', 'localedata.pyi', 'support.pyi', 'lists.pyi', 'plural.pyi', 'core.pyi', 'dates.pyi', 'languages.pyi', 'util.pyi', '__init__.pyi', '_compat.pyi', 'units.pyi', 'localtime/_unix.pyi', 'localtime/_win32.pyi', 'localtime/__init__.pyi', 'messages/extract.pyi', 'messages/mofile.pyi', 'messages/plurals.pyi', 'messages/pofile.pyi', 'messages/catalog.pyi', 'messages/checkers.pyi', 'messages/jslexer.pyi', 'messages/__init__.pyi', 'messages/frontend.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
