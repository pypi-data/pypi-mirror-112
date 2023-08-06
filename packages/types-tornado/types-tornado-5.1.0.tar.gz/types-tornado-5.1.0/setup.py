from setuptools import setup

name = "types-tornado"
description = "Typing stubs for tornado"
long_description = '''
## Typing stubs for tornado

This is a PEP 561 type stub package for the `tornado` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `tornado`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/tornado. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a90573feb2af118d224d9b9baf6cb7a3e2b0c64a`.
'''.lstrip()

setup(name=name,
      version="5.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['tornado-python2-stubs'],
      package_data={'tornado-python2-stubs': ['httpclient.pyi', 'web.pyi', 'process.pyi', 'concurrent.pyi', 'testing.pyi', 'httputil.pyi', 'httpserver.pyi', 'tcpserver.pyi', 'netutil.pyi', 'locks.pyi', 'util.pyi', '__init__.pyi', 'gen.pyi', 'ioloop.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
