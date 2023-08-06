# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daml_dit_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'dazl>=7,<8']

setup_kwargs = {
    'name': 'daml-dit-api',
    'version': '0.4.5',
    'description': 'Daml Hub DIT File API Package',
    'long_description': "daml-dit-api\n====\n\nAPI definitions for DIT packages to be hosted in Daml Hub. This mainly\ncontains the [type definitions](daml_dit_api/package_metadata.py)\nfor the format of the `dabl-meta.yaml` file at the root of each DIT file.\n\nDIT files are also used to contain integrations loaded and run by Daml\nHub. This repository also contains documentation (in this `README`)\ndescribing the runtime environment that Daml Hub provides to\nintegrations.\n\n# Package Metadata\n\nAt their core, DIT files are [ZIP archives](https://en.wikipedia.org/wiki/Zip_(file_format))\nthat follow a specific set of conventions regarding their content. The\nmost important of these conventions is the presence of a YAML metadata\nfile at the root of the archive and named `dabl-meta.yaml`. This\nmetadata file contains catalog information describing the contents of\nthe DIT, as well as any packaging details needed to successfully\ndeploy a DIT file into Daml Hub. An example of a deployment instruction is\na _subdeployment_. A subdeployment instructs Daml Hub to deploy a specific\nsubfile within the DIT file. A DIT file that contains an embedded DAR\nfile could use a subdeployment to ensure that the embedded DAR file is\ndeployed to the ledger when the DIT is deployed. In this way, a DIT\nfile composed of multiple artifacts (DARs, Bots, UI's, etc.) can be\nconstructed to deploy a set of artifacts to a single ledger in a\nsingle action.\n\n# Integrations\n\nIntegrations are a special case of DIT file that are augmented with\nthe ability to run as an executable within a Daml Hub cluster. This is\ndone by packaging Python [DAZL bot](https://github.com/digital-asset/dazl-client)\ncode into an [executable ZIP](https://docs.python.org/3/library/zipapp.html)\nusing [PEX](https://github.com/pantsbuild/pex) and augmenting tha\nresulting file with the metadata and other resources needed to make it\na correctly formed DIT file.\n\nLogically speaking, Daml Hub integrations are DAZL bots packaged with\ninformation needed to fit them into the Daml Hub runtime and user\ninterface. The major functional contrast between a Daml Hub integration\nand a Python Bot is that the integration has the external network\naccess needed to connect to an outside system and the Python Bot does\nnot. Due to the security implications of running within Daml Hub with\nexternal network access, integrations can only be deployed with the\napproval of DA staff.\n\n## Developing Integrations\n\nThe easiest way to develop an integration for Daml Hub is to use the\n[framework library](https://github.com/digital-asset/daml-dit-if)\nand [`ddit` build tool](https://github.com/digital-asset/daml-dit-ddit).\nThe integration framework presents a Python API closely related to the\nDAZL bot api and ensures that integrations follow the conventions\nrequired to integrate into Daml Hub.\n\n_Unless you know exactly what you are doing and why you are doing it,\nuse the framework._\n\n## The Integration Runtime Environment\n\nBy convention, integrations accept a number of environment variables\nthat specify key paramaters.  Integrations built with the framework\nuse defaults for these variables that connect to a default locally\nconfigured sandbox instance.\n\nVariables provided by Daml Hub include the following:\n\n| Variable | Default | Purpose |\n|----------|---------|---------|\n| `DAML_LEDGER_URL` | `http://localhost:6865` | Address of local ledger gRPC API |\n| `DABL_HEALTH_PORT` | 8089 | Port for HTTP endpoint. (Used for both liveness/readiness and webhooks) |\n| `DABL_JWKS_URL` | | HTTP URL for JWKS Repository |\n| `DABL_INTEGRATION_METADATA_PATH` | 'int_args.yaml' | Path to local metadata file |\n| `DABL_INTEGRATION_TYPE_ID` | | Type ID for the specific integration within the DIT to run |\n| `DABL_LEDGER_PARTY` | | Party identifier for network connection |\n| `DABL_LOG_LEVEL` | 0 | Log verbosity level - 0 up to 50, inclusive. |\n\n(Note that for legacy reasons, the ledger URL is also available under\nthe `DABL_LEDGER_URL` environment variable.)\n\n## Logging\n\nDABL integrations use the default Python logging package, and the\nframework provides specific support for controlling log level at\nruntime. To integrate properly with this logic, it is important that\nintegrations use the `integration` logger. This logger is switched from\n`INFO` level to `DEBUG` level at a `DABL_LOG_LEVEL` setting of 10 or above.\n\nThe preferred way of creating an integration logger is via the\n`getIntegrationLogger` function in the API package.\n",
    'author': 'Mike Schaeffer',
    'author_email': 'mike.schaeffer@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digital-asset/daml-dit-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
