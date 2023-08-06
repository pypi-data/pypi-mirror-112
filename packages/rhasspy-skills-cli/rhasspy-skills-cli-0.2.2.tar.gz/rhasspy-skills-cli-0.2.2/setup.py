# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhasspy_skills_cli']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.18', 'httpx==0.18.2', 'pydantic==1.8.2', 'typer==0.3.2']

entry_points = \
{'console_scripts': ['rhskill = rhasspy_skills_cli.main:app']}

setup_kwargs = {
    'name': 'rhasspy-skills-cli',
    'version': '0.2.2',
    'description': '',
    'long_description': '# Rhasspy skills cli\nThis application can be used to install, create and delete skills managed by [rhasspy skills](https://github.com/razzo04/rhasspy-skills). Can be installed using pip and depends on git to work properly.\n\n```bash\npip install rhasspy-skills-cli\n```\n# Install new skill\nTo install a new skill is very simple, you just need to specify the name. \n```bash\nrhskill install time_examples\n```\nThe application will clone the repositories passed with the flag "--repositories" by default will use the [examples repository](https://github.com/razzo04/rhasspy-skills-examples.git) and then will search for the skill with the corresponding name. You can also install a local directory or tar archive which contains the manifest.json. \n\n# Create new skill\nTo easily create a new skill you can use the sub-command create. If you pass the flag "-i", which stand for "--interactive", it will ask a series of prompt for helping the creation of the manifest.json.\n```bash\nrhskill create -i\n```\nYou can also specify which template to use, in this way will be generated a functional skill based on the selected template. For now, the template simple consists of overwriting the manifest.json of a working skill but in the future will be added new functionality. Once as be created you can test by using:\n```bash\nrhskill install path/to/skill\n```',
    'author': 'razzo04',
    'author_email': 'razzorazzo1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
