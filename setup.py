#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install python-cardgameengine
# pip install python-cardgameengine --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/python-cardgameengine
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file


tests_require = [
]

install_requires = [
]

setup(name='python-cardgameengine',
      url='https://github.com/paulocheque/python-cardgameengine',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python games',
      description='Library to help creation of Card Games.',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='0.1',
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      packages=find_packages(),
)

