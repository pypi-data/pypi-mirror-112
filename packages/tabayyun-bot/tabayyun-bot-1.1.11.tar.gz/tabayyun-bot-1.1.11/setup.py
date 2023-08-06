# -*- coding: utf-8 -*-
"""
    FS Pipeline library, to create airflow pipelines
    with operators like Spark, Hive etc.,
"""
from setuptools import setup, find_packages

setup(
    name='tabayyun-bot',
    version='1.1.11',
    description='A bot for checking indonesia news and hoaxes',
    long_description=open('README.md').read().strip(),
    author='azzambz',
    author_email='zam.badruzaman@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['pydantic==1.8.2', 'Flask==2.0.1', 'python-telegram-bot==13.7', 'pandas', 'colorama==0.4.4',
                      'termcolor==1.1.0', 'pyfiglet', 'beautifulsoup4==4.9.3', 'certifi==2020.12.5', 'chardet==4.0.0',
                      'idna==2.10', 'lxml==4.6.2', 'numpy==1.20.1', 'pandas==1.2.2', 'python-dateutil==2.8.1',
                      'pytz==2021.1', 'requests==2.25.1', 'six==1.15.0', 'soupsieve==2.2', 'urllib3==1.26.3',
                      'scikit-learn==0.24.2', 'pyopenssl==20.0.1', 'SQLAlchemy==1.4.20'],
    entry_points={
        'console_scripts': [
            'tabayyun-bot = cli.cli:handle_commands',
        ],
    },
    python_requires='>=3.6',
)
