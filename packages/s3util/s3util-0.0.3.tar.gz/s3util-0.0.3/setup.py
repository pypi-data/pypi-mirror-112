from setuptools import setup, find_packages
from os import path

with open('requirements.txt') as f:
    requirements = f.readlines()
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
  
setup(
        name ='s3util',
        version ='0.0.3',
        author ='Karan Pratap Singh',
        author_email ='karanpratapsingh43@gmail.com',
        url ='https://github.com/karannaoh/s3util',
        description ='s3util.',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                's3util = s3util.main:main'
            ]
        },
        classifiers =(
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ),
        keywords ='s3util s3',
        install_requires = requirements,
        zip_safe = False
)