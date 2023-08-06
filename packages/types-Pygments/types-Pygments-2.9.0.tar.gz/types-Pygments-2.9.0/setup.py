from setuptools import setup

name = "types-Pygments"
description = "Typing stubs for Pygments"
long_description = '''
## Typing stubs for Pygments

This is a PEP 561 type stub package for the `Pygments` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Pygments`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Pygments. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `7f320c6b9e148fb0ffc8e4e98ff207bb2fb378b7`.
'''.lstrip()

setup(name=name,
      version="2.9.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-docutils'],
      packages=['pygments-stubs'],
      package_data={'pygments-stubs': ['regexopt.pyi', 'console.pyi', 'plugin.pyi', 'filter.pyi', 'formatter.pyi', 'unistring.pyi', 'lexer.pyi', 'modeline.pyi', 'style.pyi', 'scanner.pyi', 'token.pyi', 'sphinxext.pyi', 'util.pyi', '__init__.pyi', 'cmdline.pyi', 'formatters/irc.pyi', 'formatters/latex.pyi', 'formatters/bbcode.pyi', 'formatters/html.pyi', 'formatters/img.pyi', 'formatters/svg.pyi', 'formatters/_mapping.pyi', 'formatters/pangomarkup.pyi', 'formatters/terminal.pyi', 'formatters/terminal256.pyi', 'formatters/__init__.pyi', 'formatters/rtf.pyi', 'formatters/other.pyi', 'styles/__init__.pyi', 'filters/__init__.pyi', 'lexers/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
