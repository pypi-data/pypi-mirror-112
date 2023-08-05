# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcom_232i']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'xcom-232i',
    'version': '0.1.3',
    'description': 'Python library to access Studer-Innotec Xcom-232i device through RS-232 over a serial port',
    'long_description': '# xcom-232i\n\nPython library to access Studer-Innotec Xcom-232i device through RS-232 over a serial port.\n\nNOTE: This lib is still WiP, so functionality is still limited, but feel free to create a [pull request](https://github.com/studer-innotec/xcom485i/pulls) if you want to contribute ;)\n\nDISCLAIMER: This library is NOT officially made by Studer-Innotec.\n\nThe complete official documentation is available on: \\\n[Studer-Innotec Download Center](https://www.studer-innotec.com/en/downloads/) *-> Software and Updates -> Communication protocol Xcom-232i*\n\n## Getting Started\n\n### Requirements\n\n#### Hardware\n\n- Xcom-232i connected to your installation\n- Xcom-232i connected to PC using USB to RS-232 adapter (1)\n- PC with at least USB2.0 or faster (works on Raspberry Pi 3/4 as well)\n\n(1) I personally am successfully using an adapter with the PL2303 chipset like [this one](https://www.amazon.de/dp/B00QUZY4UG)\n\n#### Software\n\n- any Linux based OS (x86 / ARM)\n- python3 >= 3.6\n- python3-pip\n\n### Installation\n\n```bash\npip3 install xcom-232i\n```\n\n**important**: make sure you select the USB to RS-232 adapter as the `socket_device`, usually on Linux it is `/dev/ttyUSB[0-9]`\n\n## Examples\n\n### Reading values\n\n```python\nfrom xcom_232i import XcomRS232\nfrom xcom_232i import constants as c\n\nIO = XcomRS232(socket_device=\'/dev/ttyUSB0\', baudrate=115200)\n\nlademodus = IO.get_value(c.OPERATION_MODE)\nbatt_phase = IO.get_value(c.BAT_CYCLE_PHASE)\nsolarleistung = IO.get_value(c.PV_POWER) * 1000 # convert from kW to W\nsonnenstunden = IO.get_value(c.NUM_SUN_HOURS_CURR_DAY)\nladestand = IO.get_value(c.STATE_OF_CHARGE) # in %\nstromprod = IO.get_value(c.PROD_ENERGY_CURR_DAY)\nbatt_strom = IO.get_value(c.BATT_CURRENT)\nbatt_spann = IO.get_value(c.BATT_VOLTAGE)\n\nprint(f"LModus: {lademodus} | Batt_Phase: {batt_phase} | Solar_P: {solarleistung} | SonnenH: {sonnenstunden} | Batt_V: {batt_spann} | SOC: {ladestand}")\n```\n\n### Writing values\n\n```python\nfrom xcom_232i import XcomRS232\nfrom xcom_232i import constants as c\n\nIO = XcomRS232(socket_device=\'/dev/ttyUSB0\', baudrate=115200)\n\n# write into RAM\nIO.set_value(c.SMART_BOOST_LIMIT, 100) # set smart boost limit\nIO.set_value(c.FORCE_NEW_CYCLE, 1, property_id=c.VALUE_QSP) # force new charge cycle\n\n# explanation for property_id:\nc.VALUE_QSP # write into Flash memory (important: you should write into flash only if you *really* need it!)\nc.UNSAVED_VALUE_QSP # write into RAM (default)\n```\n',
    'author': 'zocker_160',
    'author_email': 'zocker1600@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zocker-160/xcom-232i',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
