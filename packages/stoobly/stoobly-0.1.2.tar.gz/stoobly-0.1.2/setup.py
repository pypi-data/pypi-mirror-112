from setuptools import find_packages, setup
import pdb

setup(
    author='Michael Yen',
    author_email='michael@stoobly.com',
    description='Client agent for Stoobly',
    entry_points={
        'console_scripts': [
            'stoobly=stoobly.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        "click>=7.0.0,<8.0.0",
        "mergedeep>=1.3.0,<1.3.4",
        "mitmdump>=1.1.0,<=1.1.2",
        "pyyaml>=5.4,<=5.4.1",
        "requests>=2.25.0,<=2.25.1",
        "watchdog>=2.1.0,<=2.1.3",
    ],
    license='MIT',
    name='stoobly',
    packages=find_packages(include=[
        'stoobly', 'stoobly.*',
    ]),
    package_data={
        'stoobly': ['app/*' , 'config/*', 'public/*']
    },
    #scripts=['bin/stoobly-agent'],
    url='https://github.com/Stoobly/stoobly-agent',
    version='0.1.2',
)
