from distutils.core import setup

setup(
    name='python3-uwsgicachetop',
    version='1.1.0',
    url='https://github.com/claudiuvinttila/uwsgicachetop',
    download_url = 'https://github.com/claudiuvinttila/uwsgicachetop/archive/1.1.0.tar.gz',
    license='GPLv2',
    author='Goir',
    author_email='goir@goirware.de',
    scripts=['uwsgicachetop'],
    description='Top like utility for uwsgi caches',
    keywords = ['uwsgi', 'cache', 'top'],
    classifiers = [],
    install_requires = [
        'six',
    ],
)
