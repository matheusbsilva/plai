import setuptools
import codecs
import re

__version__ = re.findall('__version__ = "(.*)"',
                         open('plai/__init__.py').read())


setuptools.setup(
    name='plai',
    version=__version__,
    description='Programming language to create data manipulation pipelines.',
    url='https://github.com/matheusbsilva/plai',
    long_description=codecs.open('README.md', 'rb', 'utf8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "lark-parser >= 0.7.8",
        "pandas >= 1.4.0"
    ]
)
