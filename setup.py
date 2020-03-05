# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ai-in-dermatology',
    version='1.0',
    install_requires=['click'],
    description='Ranked classification of lesions in skin of color'
                'with deep neural networks using transfer learning and'
                'patch transformation with computer vision and GANs',
    long_description=readme,
    author='Ekaba Bisong, Eshan Henshaw, Trisha Thompson',
    author_email='dvdbisong@gmail.com',
    url='https://github.com/dvdbisong/ai-in-dermatology',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "ml = ml.cli:main"
        ]
    },
)

