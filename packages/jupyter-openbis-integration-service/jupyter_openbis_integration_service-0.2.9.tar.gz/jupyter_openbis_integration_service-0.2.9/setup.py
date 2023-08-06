import os

from setuptools import setup

setup(
    name='jupyter_openbis_integration_service',
    version='0.2.9',
    description='A webservice to create jupyter notebooks in the users home directory',
    url='https://sissource.ethz.ch/sis/jupyter-openbis-integration/',
    author='SIS | ID | ETH Zuerich',
    author_email='swen@ethz.ch',
    license='BSD',
    packages=['jupyter_openbis_integration_service'],
    install_requires=[
        'tornado',
    ],
    zip_safe=False,
    entry_points='''
         [console_scripts]
         jupyter_openbis_integration_service=jupyter_openbis_integration_service.server:start_server
    '''
)
