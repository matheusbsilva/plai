import setuptools
import codecs


setuptools.setup(
    name='plAI',
    version='0.0.0',
    description='Programming language to create machine learning pipelines.',
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
        "lark-parser == 0.7.8",
        "pandas == 0.25.3"
        ]
)
