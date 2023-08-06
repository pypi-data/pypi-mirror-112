from setuptools import setup

name = "types-vobject"
description = "Typing stubs for vobject"
long_description = '''
## Typing stubs for vobject

This is a PEP 561 type stub package for the `vobject` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `vobject`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/vobject. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a7446632f71aa3fb69b00019887506b4d184e423`.
'''.lstrip()

setup(name=name,
      version="0.9.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['vobject-stubs'],
      package_data={'vobject-stubs': ['vcard.pyi', 'hcalendar.pyi', 'base.pyi', 'icalendar.pyi', 'win32tz.pyi', 'ics_diff.pyi', 'behavior.pyi', '__init__.pyi', 'change_tz.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
