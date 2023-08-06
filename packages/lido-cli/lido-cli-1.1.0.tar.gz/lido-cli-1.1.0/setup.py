# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lido_validate_keys']
install_requires = \
['click==8.0.1', 'colorama==0.4.4', 'lido==1.1.0']

entry_points = \
{'console_scripts': ['lido-cli = lido_validate_keys:cli']}

setup_kwargs = {
    'name': 'lido-cli',
    'version': '1.1.0',
    'description': 'Lido CLI tool for node operator key validation',
    'long_description': '# Node Operator Key Checker CLI\n\n## Installation\n\nYou can get this tool using `pip`:\n\n```\npip install lido-cli\n```\n\nOr if you cloned this repository, install Python dependencies via:\n\n```\n./init.sh\n```\n\n## Running\n\n### RPC Provider\n\nThis is the only thing required, the rest will be handled automatically unless overridden.\n\n```\npython3 lido_validate_keys.py --rpc https://mainnet.provider.io/v3/XXX validate_network_keys\n```\n\n### Optional Parameters\n\nBy default CLI will use embedded strings and ABIs, but you can specify your own arguments if needed. Make sure to use them on CLI itself and not on the command eg:\n\n```\npython lido_validate_keys.py --rpc https://mainnet.provider.io/v3/XXX --max_multicall 300 --lido_address 0x123 --lido_abi_path /Users/x/xx.json --registry_address 0x123 --registry_abi_path /Users/x/xx.json validate_network_keys\n```\n\n```\n--rpc                                   RPC provider for network calls.\n--max_multicall\t\t\t\tBatch amount of function calls to fit into one RPC call.\n--lido_address\t\t\t\tAddress of the main contract.\n--lido_abi_path\t\t\t\tABI file path for the main contract.\n--registry_address\t\t\tAddress of the operator contract.\n--registry_abi_path\t\t\tABI file path for operators contract.\n```\n\n### Checking Network Keys\n\nCommand: `validate_network_keys`\n\nExample:\n\n```\npython lido_validate_keys.py --rpc https://mainnet.provider.io/v3/XXX validate_network_keys\n```\n\n### Checking Keys from File\n\nCommand: `validate_file_keys`\nSpecify the input file via `--file` or copy it as `input.json` to the cli folder\n\nExample with default file location:\n\n```\npython lido_validate_keys.py --rpc https://mainnet.provider.io/v3/XXX validate_file_keys\n```\n\nExample with custom file path:\n\n```\npython lido_validate_keys.py --rpc https://mainnet.provider.io/v3/XXX validate_file_keys --file input.json\n```\n\nYou can also get all commands and options via `python lido_validate_keys.py --help`\n',
    'author': 'Lido',
    'author_email': 'info@lido.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lido.fi',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7.1,<4',
}


setup(**setup_kwargs)
