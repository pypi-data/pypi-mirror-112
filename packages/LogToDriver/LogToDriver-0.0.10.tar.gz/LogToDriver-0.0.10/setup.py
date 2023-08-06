from setuptools import setup

setup(
    name='LogToDriver',
    version='0.0.10',
    packages=['LogToDriver'],
    keywords=['LogToDriver'],
    install_requires=[
        'elasticsearch==7.13.2',
        'robotframework==4.0.3',
        'pytz==2021.1'
    ],
)
