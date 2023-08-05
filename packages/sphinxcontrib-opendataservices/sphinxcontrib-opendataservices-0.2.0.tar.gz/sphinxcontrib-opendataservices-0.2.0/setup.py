from setuptools import setup

setup(
    name='sphinxcontrib-opendataservices',
    version='0.2.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    packages=['sphinxcontrib'],
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices',
    install_requires=[
        'docutils',
        'jsonpointer',
        'myst-parser',
        'sphinx',
        'sphinxcontrib-opendataservices-jsonschema',
    ],
    extras_require={
        'test': [
            'coveralls',
            'flake8',
            'isort',
            'lxml',
            'pytest',
            'pytest-cov',
        ],
    },
    namespace_packages=['sphinxcontrib'],
)
