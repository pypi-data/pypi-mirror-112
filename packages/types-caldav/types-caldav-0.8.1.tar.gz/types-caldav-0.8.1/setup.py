from setuptools import setup

name = "types-caldav"
description = "Typing stubs for caldav"
long_description = '''
## Typing stubs for caldav

This is a PEP 561 type stub package for the `caldav` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `caldav`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/caldav. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8d12d6f4689351f6856ad79961db9a200552b845`.
'''.lstrip()

setup(name=name,
      version="0.8.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-requests', 'types-vobject'],
      packages=['caldav-stubs'],
      package_data={'caldav-stubs': ['davclient.pyi', 'objects.pyi', '__init__.pyi', 'elements/dav.pyi', 'elements/cdav.pyi', 'elements/base.pyi', 'elements/ical.pyi', 'elements/__init__.pyi', 'lib/url.pyi', 'lib/error.pyi', 'lib/namespace.pyi', 'lib/__init__.pyi', 'lib/vcal.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
