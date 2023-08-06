from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.1'
DESCRIPTION = 'Argon2 helper'

# Setting up
setup(
    name="dzh",
    version=VERSION,
    author="Daduz",
    author_email="<davide.tropea97@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['argon2-cffi', 'cffi', 'colorama', 'django-qrcode', 'Pillow', 'pycparser', 'pyperclip', 'qrcode[pil]', 'six'],
    keywords=['python', 'daduz'],
    entry_points={'console_scripts':['dzh=dzh:__main__']},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)