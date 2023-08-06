from setuptools import setup, find_packages

packages = find_packages('src')
setup(
    name='ekster',
    version='0.3.0a',
    description='Ekster star formation simulations',
    url='https://github.com/rieder/ekster',
    author='Steven Rieder',
    author_email='steven+ekster@rieder.nl',
    license='Apache License 2.0',
    packages=packages,
    package_dir={'': 'src'},
    install_requires=[
        'amuse-framework>=2021.7.0',
        'amuse-seba>=2021.7.0',
        'amuse-fi>=2021.7.0',
        'amuse-petar>=2021.7.0',
        'amuse-phantom>=2021.7.0',
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Fortran',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
)
