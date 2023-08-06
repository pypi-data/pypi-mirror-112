# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testsuite', 'testsuite.tests']

package_data = \
{'': ['*']}

install_requires = \
['lxml==4.6.3']

entry_points = \
{'console_scripts': ['testsuite = testsuite.console:main']}

setup_kwargs = {
    'name': 'testsuite',
    'version': '0.1.2',
    'description': 'Example BuildingSync files and tools for writing and validating BuildingSync use cases as schematron files.',
    'long_description': '# testsuite\n\n[![PyPI version](https://badge.fury.io/py/testsuite.svg)](https://badge.fury.io/py/testsuite)\n\n![example workflow](https://github.com/buildingsync/testsuite/actions/workflows/ci.yml/badge.svg?branch=develop)\n\nA tool for writing and validating BuildingSync use cases as Schematron files.\nSee the [BuildingSync use-cases](https://github.com/BuildingSync/use-cases) repository for current Schematron and example files for particular use cases.\n\n## Command line validation\n### Setup\n#### Install from pypi\n```bash\npip install testsuite\n```\n#### Install from source\n[Poetry](https://python-poetry.org/) is required to install testsuite.\n```bash\n# Copy repo\ngit clone https://github.com/BuildingSync/TestSuite.git\n\n# install the package\ncd TestSuite\npoetry install\n\n# Test that it works, you should see a message describing the usage\npoetry run testsuite\n```\n\n## Usage\n### Python\n```python\nfrom testsuite.validate_sch import validate_schematron\n\n# run basic validation\n# returns an array of testsuite.validate_sch.Failures\nfailures = validate_schematron(\'my_schematron.sch\', \'my_xml.xml\')\n\n# save the svrl result file\nfailures = validate_schematron(\'my_schematron.sch\', \'my_xml.xml\', result_path=\'validation_result.svrl\')\n\n# run a specific phase in schematron\nfailures = validate_schematron(\'my_schematron.sch\', \'my_xml.xml\', phase=\'MyPhaseID\')\n\n# report unfired rules as errors\nfailures = validate_schematron(\'my_schematron.sch\', \'my_xml.xml\', strict_context=True)\n```\n\n### CLI\n```bash\ntestsuite validate my_schematron.sch my_xml.xml\n\n# see all options\ntestsuite validate --help\n```\n\n## Development\n### Generate Schematron\nFirst create a CSV file that meets the required structure:\n```\nphase title,phase see,pattern title,pattern see,rule title,rule context,assert test,assert description,assert severity,notes\n```\nSee the CSV files in this repo for examples.\n\nHierarchy is implied by the lack of text in a column. If no phase data is added to a row, it\'s considered to be the same phase as the row above. If no pattern data is present, it\'s assumed to be the same pattern as above. If no rule context is given, it\'s assumed to be the same as the one above.\n\nThe generator expects a "exemplary" xml file which should pass the validation. This is used to make sure all rules are applied (schematron will skip rules if the rule context doesn\'t match or if it only matches nodes that have already been matched within that pattern). If no exemplary file is provided no rule context checks will be made.\n```bash\npoetry run testsuite generate path_to_csv [path_to_exemplary_xml]\n```\n\n### Testing\n```bash\npoetry run tox -e python\n```\n',
    'author': 'Ted Summer',
    'author_email': 'ted@devetry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://buildingsync.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
