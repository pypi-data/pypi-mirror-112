# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import auth_rename

setup(
    name='auth-rename',
    version=auth_rename.__version__,
    description='to rename authentication and authorization to user management',
    long_description='to rename authentication and authorization',
    long_description_content_type='text/x-rst',
    author='malinka',
    author_email='malinkaphann@gmail.com',
    include_package_data=True,
    url='https://github.com/malinkaphann/auth-rename/tree/%s' % auth_rename.__version__,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)

# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI
