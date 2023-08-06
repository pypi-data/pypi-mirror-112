# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_bundle_plugin',
 'poetry_bundle_plugin.bundlers',
 'poetry_bundle_plugin.console',
 'poetry_bundle_plugin.console.commands',
 'poetry_bundle_plugin.console.commands.bundle']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a1,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['export = '
                               'poetry_bundle_plugin.plugin:BundleApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-bundle-plugin',
    'version': '0.1.0',
    'description': 'Poetry plugin to bundle projects into various formats',
    'long_description': '# Poetry bundle plugin\n\nThis package is a plugin that allows the bundling of Poetry projects into various formats.\n\n\n## Installation\n\nThe easiest way to install the `bundle` plugin is via the `plugin add` command of Poetry.\n\n```bash\npoetry plugin add poetry-bundle-plugin\n```\n\nIf you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.\n\n```bash\npipx inject poetry poetry-bundle-plugin\n```\n\nOtherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.\n\n```bash\npip install poetry-bundle-plugin\n```\n\n\n## Usage\n\nThe plugin introduces a `bundle` command namespace that regroups commands to bundle the current project\nand its dependencies into various formats. These commands are particularly useful to deploy\nPoetry-managed applications.\n\n### bundle venv\n\n### bundle venv\n\nThe `bundle venv` command bundles the project and its dependencies into a virtual environment.\n\nThe following command\n\n```bash\npoetry bundle venv /path/to/environment\n```\n\nwill bundle the project in the `/path/to/environment` directory by creating the virtual environment,\ninstalling the dependencies and the current project inside it. If the directory does not exist,\nit will be created automatically.\n\nBy default, the command uses the current Python executable to build the virtual environment.\nIf you want to use a different one, you can specify it with the `--python/-p` option:\n\n```bash\npoetry bundle venv /path/to/environment --python /full/path/to/python\npoetry bundle venv /path/to/environment -p python3.8\npoetry bundle venv /path/to/environment -p 3.8\n```\n\n**Note**\n\nIf the virtual environment already exists, two things can happen:\n\n- **The python version of the virtual environment is the same as the main one**: the dependencies will be synced (updated or removed).\n- **The python version of the virtual environment is different**: the virtual environment will be recreated from scratch.\n\nYou can also ensure that the virtual environment is recreated by using the `--clear` option:\n\n```bash\npoetry bundle venv /path/to/environment --clear\n```\n',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
