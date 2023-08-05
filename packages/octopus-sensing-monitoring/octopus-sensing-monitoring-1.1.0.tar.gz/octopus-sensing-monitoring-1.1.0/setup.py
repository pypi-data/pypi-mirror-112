# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_sensing_monitoring']

package_data = \
{'': ['*'], 'octopus_sensing_monitoring': ['ui_build/*']}

install_requires = \
['CherryPy>=18.6.0,<19.0.0', 'Pillow>=8.2.0,<9.0.0', 'numpy>=1.21.0,<2.0.0']

entry_points = \
{'console_scripts': ['octopus-sensing-monitoring = '
                     'octopus_sensing_monitoring.main:main']}

setup_kwargs = {
    'name': 'octopus-sensing-monitoring',
    'version': '1.1.0',
    'description': 'Web base data monitoring/visualizer for https://octopus-sensing.nastaran-saffar.me',
    'long_description': 'Octopus Sensing Monitoring\n==========================\n\nA web-based real-time monitoring for [Octopus Sensing](https://octopus-sensing.nastaran-saffar.me/). You can\nmonitor your data from any machine in the same network.\n\nInstallation\n------------\n\nIt required Python 3.7 or later. And it needs to be installed on the same machine where `Octopus\nSensing` is running.\n\nYou can use `pip` to install it:\n\n```\npip install octopus-sensing-monitoring\n```\n\nThen simply run it by invoking `octopus-sensing-monitoring` from the command line.\n\nYou can also use one of the Python package managers like [pipenv](https://pipenv.pypa.io/en/latest/)\nor [poetry](https://python-poetry.org/) to prevent package conflict.\n\n```\npipenv install octopus-sensing-monitoring\npipenv run octopus-sensing-monitoring\n```\n\nThe monitoring will listen on `8080` port. Open a web page and point to the machine\'s IP. For\nexample, in the same machine, open http://localhost:8080 . Or replace `localhost` with the machine\'s\nIP and open it from any other machine.\n\nTesting with fake data\n----------------------\n\nFor testing purposes, you can ask the server to generate fake data instead of fetching data from\n`Octopus Sensing`. To do so, add `--fake` flag when running the script:\n\n```\noctopus-sensing-monitoring --fake\n```\n\nNaming your devices\n-------------------\n\nIn `Octopus Sensing`, when you\'re creating instance of devices, you need to provide a `name`. At the\nmoment, device names are hard coded in this monitoring app. So you need to use these names for your\ndevices in order for them to appear on the web page.\n\n* For OpenBCIStreaming use `eeg` (i.e. `OpenBCIStreaming(name="eeg", ...)` )\n* For Shimmer3Streaming use `shimmer`\n* For the webcam, you need to create instance of `MonitoredWebcam` and name it `webcam`\n\nSecurity notice\n---------------\n\nNote that the web server accepts requests from any machine, and it uses `http` protocol which\nis not encrypted. Don\'t run it on a network that you don\'t trust.\n\nCopyright\n---------\n\nCopyright © 2020,2021 [Aidin Gharibnavaz](https://aidinhut.com)\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU\nGeneral Public License as published by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nSee [License file](LICENSE) for full terms.\n',
    'author': 'Aidin Gharibnavaz',
    'author_email': 'aidin@aidinhut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidin36/octopus-sensing-monitoring',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
