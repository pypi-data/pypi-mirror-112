from setuptools import setup

setup(
    name='ElasticSearchHandler',
    version='0.0.1',
    packages=['ElasticSearchHandler'],
    install_requires=['elasticsearch7'],
    requires=[],
    url='https://github.com/oleglpts/ElasticSearchHandler',
    license='MIT',
    platforms='any',
    author='Oleg Lupats',
    author_email='oleglupats@gmail.com',
    description='Elasticsearch handler for logging',
    long_description='Standard logging handler module for sending logs to Elasticsearch',
    classifiers=['Programming Language :: Python :: 3']
)
