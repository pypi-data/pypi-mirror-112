from setuptools import setup
release_version = '0.0.3'

setup(
    name='perfecto-py3',
    packages=['perfecto','perfecto/client', 'perfecto/Exceptions', 'perfecto/model', 'perfecto/test'],  # this must be the same as the name above
    package_data = {'': ['*.txt']},
	version=release_version,
    description='Perfecto Reporting SDK for Python\nPerfecto Reporting is a multiple execution digital report',
    author='Perfecto',
    author_email='perfecto@perfectomobile.com',
    url='https://github.com/PerfectoCode',  # use the URL to the GitHub repo
    download_url='https://github.com/PerfectoCode',
    keywords=['Perfecto', 'PerfectoMobile', 'Reporting', 'Selenium', 'Appium', 'Automation testing'],
    classifiers=[ 'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent']
)