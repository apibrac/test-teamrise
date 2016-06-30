try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Test for teamrise interviews',
    'author': 'Alexis Pibrac',
    'url': 'https://github.com/apibrac/test-teamrise',
    'download_url': 'https://github.com/apibrac/test-teamrise',
    'author_email': 'alexis.pibrac@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': [],
    'scripts': [],
    'name': 'test_teamrise'
}

setup(**config)