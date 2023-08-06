# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neogiinstruments', 'neogiinstruments.camera', 'neogiinstruments.rotator']

package_data = \
{'': ['*']}

install_requires = \
['Instrumental-lib>=0.6,<0.7',
 'PyMeasure>=0.9.0,<0.10.0',
 'PyVISA-py>=0.5.2,<0.6.0',
 'h5py>=3.3.0,<4.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'nidaqmx>=0.5.7,<0.6.0',
 'pandas>=1.3.0,<2.0.0',
 'panel>=0.11.3,<0.12.0',
 'param>=1.10.1,<2.0.0',
 'pigpio>=1.78,<2.0',
 'plotly>=5.0.0,<6.0.0',
 'pyserial>=3.5,<4.0',
 'pyusb>=1.2.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['port_table = neogiinstruments.ports:port_table']}

setup_kwargs = {
    'name': 'neogiinstruments',
    'version': '2.3.0',
    'description': 'Communication and helper functions for lab equipment',
    'long_description': '# Instruments\n\nCommunication and helper functions for lab equipment  \nIf you\'re reading this, this is a WIP new class-based system of autodetecing instruments and exposing common APIs\n\n## Creating instruments\n\n1. individual files in neoginstruments will be seperate instruments\n2. folders designate interchangeable instruments with common apis\n    1. Each folder will result in automatic selection of a instrument\n    2. Each folder will use and document an API\n3. Each valid instruments file must have a\n    1. name\n    2. hwid: array of valid hardware IDs (for linux)\n        1. use lsusb to get them. IE:"0403:FAF0"\n        2. use "software" to create a virtual instrument\n    3. instrument class\n        1. Must accept the port as its only argument in `__init__`. You can get the serial with port.serial_number\n\n## Using instruments\n\nExample:\n\n```\nimport neogiinstruments  \nrotator = neogiinstruments.rotator("rotator1") #creates rotator named rotator1\nrotator.instrument_selected = \'55114654 - ttyUSB7 - K10CR1\' \nrotator.instrument.home() #homes the rotator\nrotator.update_to_serial()\n```\n\nEach module will return its respective instrument. Multiple distinct verisons of the same instrument can exist.   \nYou can either manually change instrument_selected or use `.view()` to make an interactive GUI.  \nAll functions of each instrument are avalible through the `.instrument` sub-object.\n    \n\n## Utilities\nyou can call port_table() to print a port table',
    'author': 'UNT Neogi Lab',
    'author_email': 'BrianSquires@my.unt.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
