import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nxpprog',
    version='1.0.1',
    author='SJSU-Dev2 Organization',
    description='Programmer for NXP arm processors using ISP protocol.',long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SJSU-Dev2/nxpprog/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': ['nxpprog=nxpprog.nxpprog:main'],
    },
    python_requires='>=3.9',
    install_requires=[
      'pyserial>=3.4',
      'click>=7.1.2',
    ]
)
