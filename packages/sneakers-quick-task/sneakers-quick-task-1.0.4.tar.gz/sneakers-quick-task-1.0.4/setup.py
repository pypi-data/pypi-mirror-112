from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="sneakers-quick-task",
    version="1.0.4",
    description="A simple API for generating Sneakers AIO Quick Task URLs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://sneakersaio.com',
    author="Sneakers AIO, Inc.",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='sneakers, aio, quick, task, url',
    packages=find_packages(include=['sneakersaio']),
    python_requires='>=3.0, <4',
    project_urls={
        'Bug Reports': 'https://github.com/Sneakers-AIO/Sneakers-AIO-Quick-Task-API/issues',
        'Source': 'https://github.com/Sneakers-AIO/Sneakers-AIO-Quick-Task-API'
    }
)
