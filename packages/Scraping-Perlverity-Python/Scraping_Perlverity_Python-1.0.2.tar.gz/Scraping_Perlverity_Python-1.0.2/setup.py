from setuptools import setup


requires = ["requests>=2.14.2"]

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Scraping_Perlverity_Python',
    version='1.0.2',
    description='pip install Success!! pip install でライブラリインストールでWebスクレイピング起動可能。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Perlverity/Python_Scraping_pip_install',
    author='Perlverity',
    author_email='perlverity@gmail.com',
    license='MIT',
    keywords='sample setuptools development',
    packages=[
        "Scraping_Perlverity_Python"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)