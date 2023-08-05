# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serialized_data_interface']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema==3.2', 'ops>=1.1,<2.0', 'pyyaml==5.3', 'requests==2.25']

setup_kwargs = {
    'name': 'serialized-data-interface',
    'version': '0.3.0',
    'description': 'Serialized Data Interface for Juju Operators',
    'long_description': "# Serialized Data Interface Library\n\nhttps://pypi.org/project/serialized-data-interface/\n\nThis libraries enables its user to create serialized and validated Juju Operator interfaces.\n\nAn interface Schema will be defined through YAML e.g:\n\n```yaml\nv1:\n  provides:\n    type: object\n    properties:\n      access-key:\n        type: string\n      namespace:\n        type: ['string', 'null']\n      port:\n        type: number\n      secret-key:\n        type: string\n      secure:\n        type: boolean\n      service:\n        type: string\n    required:\n      - access-key\n      - port\n      - secret-key\n      - secure\n      - service\n```\n\nWhen our charms interchange data, this library will validate the data through the schema on both ends.\n\n# Usage\nIn our charm metadata we would add the following lines to define our schema and the supported versions:\n\n```yaml\nprovides:\n  oidc-client:\n    interface: oidc-client\n    schema: https://raw.githubusercontent.com/canonical/operator-schemas/oidc-schemas/oidc-client.yaml\n    versions: [v1]\n```\n\nIn this case SDI will pull the schema from Github during deployment. If we want to deploy our charm in environments where Github isn't available we can pull the schemas during our build process by adding some lines like this in our `tox.ini` file:\n\n```\n[testenv:build]\ncommands =\n    charmcraft build\n    python3 -m serialized_data_interface.local_sdi\n```\n\n# Real World Example\n\n* Minio with Provider Interface\n  * https://github.com/canonical/minio-operator/\n* Argo Controller with Requirer Interface:\n  * https://github.com/canonical/argo-operators/\n\n# TODO\n\n* Currently only provides data to App relations, should also support unit relations.\n",
    'author': 'Dominik Fleischmann',
    'author_email': 'dominik.fleischmann@canonical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/canonical/serialized-data-interface/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
