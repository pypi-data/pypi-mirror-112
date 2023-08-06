import json
import os

import setuptools

loc = os.path.dirname(os.path.abspath(__file__))


def get_description():
    info = 'THIS IS A FORK OF THE ORIGINAL WITH MINOR CHANGES!\n\n'
    with open(loc + '/docs/README.rst') as readme:
        info = info + readme.read()
    with open(loc + '/docs/changelog.rst') as changelog:
        return info + '\n\n' + changelog.read()


with open(loc + '/requirements.txt') as f:
    required = f.read().splitlines()

with open('lemonadefashion_flask_monitoringdashboard/constants.json', 'r') as f:
    constants = json.load(f)

setuptools.setup(
    name="lemonadefashion-Flask-MonitoringDashboard",
    version=constants['version'],
    setup_requires=['setuptools_scm'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    test_suite='tests.get_test_suite',
    url='https://github.com/us88/Flask-MonitoringDashboard',
    author=constants['author'],
    author_email=constants['email'],
    description="Automatically monitor the evolving performance of Flask/Python web services.",
    long_description=get_description(),
    install_requires=required,
    entry_points={'flask.commands': ['fmd=lemonadefashion_flask_monitoringdashboard.cli:fmd']},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Flask',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/us88/Flask-MonitoringDashboard/issues',
        'PyPi': 'https://pypi.org/project/lemonadefashion-Flask-MonitoringDashboard/',
        'Documentation': 'http://flask-monitoringdashboard.readthedocs.io/',
        'Source': 'https://github.com/us88/Flask-MonitoringDashboard/',
    },
)
