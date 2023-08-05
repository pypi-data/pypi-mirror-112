# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mail_handler']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0']

entry_points = \
{'console_scripts': ['render_mail = mail_handler.render_mail:main',
                     'send_mail = mail_handler.send_mail:main']}

setup_kwargs = {
    'name': 'pycontw-mail-handler',
    'version': '0.4.0',
    'description': 'Mail toolkit for PyCon Taiwan',
    'long_description': '# Mail Handler\n\nGenerate emails through the template and send mails\n\n## Prerequisite\n\n* [Python 3](https://www.python.org/downloads/)\n* [click](http://click.palletsprojects.com/en/7.x/)\n\n## Usage\n\nThis CLI tool is designed as two steps to avoid accidental sending.\n\n### Step 1: Install pycontw-mail-handler through pipx (or install in your virtual environment)\n\n```sh\n# Install pipx\npython -m pip install pipx\n\n# Install pycontw-mail-hanlder through pipx\npython -m pipx install pycontw-mail-handler\n```\n\nAfter install `pycontw-mail-handler`, you can run `render_mail` and `send_mail` commands in your environment.\n\n### Step 2: Generate mails through the template\n\n```sh\nrender_mail [OPTIONS] TEMPLATE_PATH RECEIVER_DATA\n\nOptions:\n  --mails_path PATH  [default: mails_to_sent]\n  --separator \' TEXT \'\n```\n\n* `TEMPLATE_PATH`: The path to the jinja2 template.\n* `RECEIVER_DATA`: The path to receivers\' data.\n    * The following json sample is the least required content. All other data can be added to fit the need of the template.\n    * "common_data": Common data used in each mail\n    * "unique_data": Unique content for each mail\n\n```json\n{\n    "common_data": {},\n    "unique_data": [\n        {"receiver_email": "somerec@somedomain"}\n    ]\n}\n```\n\nPlease note the comma is able to be used as a receiver separator to send multiple people. For example, the following 3\nformats are all working:\n\nA space following a comma\n```json\n{\n    "common_data": {},\n    "unique_data": [\n        {"receiver_email": "somerec01@somedomain, somerec02@somedomain"}\n    ]\n}\n```\n\nNo space following a comma\n```json\n{\n    "common_data": {},\n    "unique_data": [\n        {"receiver_email": "somerec01@somedomain,somerec02@somedomain"}\n    ]\n}\n```\n\nOr mix both of the above two types\n```json\n{\n    "common_data": {},\n    "unique_data": [\n        {"receiver_email": "somerec01@somedomain, somerec02@somedomain,somerec03@somedomain"}\n    ]\n}\n```\n\n\n* `--mails_path PATH`: The output path of the mails. The mail will be named as the receivers email address.\n\nUsage example:\n\n```\nrender_mail  ./templates/sponsorship/spam_sponsors_2020.j2 examples/sponsorship/spam_sponsors_2020.json\n```\n\n\n### Step 3: Send the generated mails\n\n```sh\nsend_mail [OPTIONS] CONFIG_PATH\n\nOptions:\n  --mails_path PATH  [default: mails_to_sent]\n  --attachment_file PATH\n```\n\n* `CONFIG_PATH`: The path to mail config.\n\n```json\n{\n    "Subject": "some subject",\n    "From": "somebody@somedomain",\n    "CC": "somebody1@somedomain, somebody2@somedomain"\n}\n```\n\nPlease note the comma is used as a receiver separator to send multiple people.\n\n* `--mails_path PATH`: The path of the mails to sent.\n\nUsage example:\n\n```\nsend_mail ./examples/sponsorship/spam_sponsors_2020_mail_config.json\n```\n\n\nBy issuing the `send_mail.py` command,\nyou will be prompted to input the corresponding password of your smtp server.\n\n```plaintext\nYou are about to send the mails under "mails_to_sent". Do you want to continue? [y/N]: y\nPlease enter your mail account: <sender email address in mail config>\nPlease enter you mail password:\nINFO:root:Email sent to <receiver address in RECEIVER_DATA>!\n```\n\nCurrently we only support the smtp server of `gmail`,\nso you may want to use the one-time app password for security concern.\nTo use gmail one-time app password, please go to\n`Manage your Goolge Account > Security > Signning to Google > App passwords` and then\n`Select app > Other`\nto generate your one-time app password. The generated password could be removed anytime\nif you are sure that you won\'t use it anymore.\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\n\n[Lee-W](https://github.com/Lee-W)\n',
    'author': 'Lee-W',
    'author_email': 'weilee.rx@gmail.com',
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
