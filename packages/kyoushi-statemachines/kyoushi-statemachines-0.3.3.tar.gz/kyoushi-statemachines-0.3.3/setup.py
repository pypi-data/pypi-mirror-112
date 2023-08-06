# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cr_kyoushi',
 'cr_kyoushi.statemachines',
 'cr_kyoushi.statemachines.aecid_attacker',
 'cr_kyoushi.statemachines.beta_user',
 'cr_kyoushi.statemachines.core',
 'cr_kyoushi.statemachines.horde_user',
 'cr_kyoushi.statemachines.owncloud_user',
 'cr_kyoushi.statemachines.ssh_user',
 'cr_kyoushi.statemachines.web_browser',
 'cr_kyoushi.statemachines.wordpress_editor',
 'cr_kyoushi.statemachines.wordpress_wpdiscuz']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=5.6.5,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'email-validator>=1.1.2,<2.0.0',
 'idna>=2.8,<3.0',
 'kyoushi-simulation>=0.3.8,<0.4.0',
 'numpy>=1.19.5,<2.0.0',
 'pwntools>=4.3.1,<5.0.0',
 'selenium>=3.141.0,<4.0.0',
 'titlecase>=2.0.0,<3.0.0',
 'webdriver-manager>=3.2.2,<4.0.0']

entry_points = \
{'kyoushi.simulation': ['ait.aecid.attacker.wpdiscuz = '
                        'cr_kyoushi.statemachines.aecid_attacker:StatemachineFactory',
                        'ait.beta_user = '
                        'cr_kyoushi.statemachines.beta_user:StatemachineFactory',
                        'ait.horde_user = '
                        'cr_kyoushi.statemachines.horde_user:StatemachineFactory',
                        'ait.owncloud_user = '
                        'cr_kyoushi.statemachines.owncloud_user:StatemachineFactory',
                        'ait.ssh_user = '
                        'cr_kyoushi.statemachines.ssh_user:StatemachineFactory',
                        'ait.web_browser = '
                        'cr_kyoushi.statemachines.web_browser:StatemachineFactory',
                        'ait.wordpress_editor = '
                        'cr_kyoushi.statemachines.wordpress_editor:StatemachineFactory',
                        'ait.wordpress_wpdiscuz = '
                        'cr_kyoushi.statemachines.wordpress_wpdiscuz:StatemachineFactory']}

setup_kwargs = {
    'name': 'kyoushi-statemachines',
    'version': '0.3.3',
    'description': '',
    'long_description': '# Cyber Range Kyoushi - State Machines\n\nUser simulation state machines for the AIT Cyber Range and AECID testbeds.\n',
    'author': 'Maximilian Frank',
    'author_email': 'maximilian.frank@ait.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ait-aecid.github.io/kyoushi-statemachines',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
