# Licensed under a 3-clause BSD style license - see LICENSE.rst
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

from Ska.engarchive.version import package_version

try:
    from testr.setup_helper import cmdclass
except ImportError:
    cmdclass = {}

# Write GIT revisions and SHA tag into <this_package/git_version.py>
# (same directory as version.py)
package_version.write_git_version_file()


setup(name='Ska.engarchive',
      author='Tom Aldcroft',
      description='Modules supporting Ska engineering telemetry archive',
      author_email='aldcroft@head.cfa.harvard.edu',
      entry_points={'console_scripts': ['ska_fetch = Ska.engarchive.get_telem:main']},
      py_modules=['Ska.engarchive.fetch', 'Ska.engarchive.converters', 'Ska.engarchive.utils',
                  'Ska.engarchive.get_telem'],
      version=package_version.version,
      zip_safe=False,
      packages=['Ska', 'Ska.engarchive', 'Ska.engarchive.derived', 'Ska.engarchive.tests'],
      package_dir={'Ska': 'Ska'},
      package_data={'Ska.engarchive': ['*.dat', 'units_*.pkl', 'GIT_VERSION'],
                    'Ska.engarchive.tests': ['*.dat']},
      tests_require=['pytest'],
      cmdclass=cmdclass,
      )
