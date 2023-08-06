import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='simantha',
    version='0.1.1',
    author='Michael Hoffman',
    author_email='m.hoff4@gmail.com',
    description='Simulation of Manufacturing Systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/m-hoff/simantha',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
