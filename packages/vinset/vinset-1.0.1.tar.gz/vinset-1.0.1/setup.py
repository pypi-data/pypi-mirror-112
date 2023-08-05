from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Command line program to draw the graph from video and csv files.'

setup(
    name='vinset',
    version='1.0.1',
    author='Zaw Lin Tun',
    author_email='zawlintun1511@gmail.com',
    url='https://github.com/jtur044/vinset',
    description='gaze visualisation program',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=None,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vinset = vinset.vin:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='gaze visualisation program vinset',
    install_requires=requirements,
    zip_safe=False
)
