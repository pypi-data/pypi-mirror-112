from setuptools import setup, Extension
import os

divsufsort = Extension(
    'divsufsort',
    sources=[
        'src/ext/divsufsort.c',
        'src/ext/sssort.c',
        'src/ext/trsort.c',
        'src/ext/utils.c',
        'src/ext.cpp'
        ],
    depends=[
        'src/ext/config.h',
        'src/ext/divsufsort.h',
        'src/ext/divsufsort_private.h',
        'src/ext/lfs.h',
        ],
    include_dirs=['src/ext'],
    define_macros=[
        ('HAVE_CONFIG_H', '1')
        ],
    )

with open('README.md', 'r') as fin:
    long_description = fin.read()

with open('VERSION', 'r') as fin:
    short_version = fin.read().strip()

setup(name = 'divsufsort',
    version = os.environ.get('VERSION', f'{short_version}.dev0'),
    description = 'Python bindings for libdivsufsort',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    author = 'Martin Vejnár',
    author_email = 'martin.vejnar@avast.com',
    url = 'https://github.com/avast/divsufsort-python',
    license = 'MIT',

    ext_modules = [divsufsort],
    )
