# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formset']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.6" and python_version < "2.7"': ['argparse>=1.4.0,<2.0.0']}

entry_points = \
{'console_scripts': ['formset = formset.formset:main']}

setup_kwargs = {
    'name': 'formtools-formset',
    'version': '1.0.0',
    'description': 'A form.set generator.',
    'long_description': 'formset\n=======\n\n[![Test](https://github.com/tueda/formset/workflows/Test/badge.svg?branch=main)](https://github.com/tueda/formset/actions?query=branch:main)\n[![PyPI version](https://badge.fury.io/py/formtools-formset.svg)](https://pypi.org/project/formtools-formset/)\n\nA `form.set` generator.\n\nThis is a small script to generate a configuration file `form.set` of\n[FORM](https://www.nikhef.nl/~form/) for your machine.\nThe script suggests adequate *static* buffer sizes for `tform` from\nthe number of CPUs and physical memory available on the computer.\n\n\nInstallation\n------------\n\n```sh\npip install formtools-formset\n```\n\nYou can also pick up the main script file [`formset.py`](https://raw.githubusercontent.com/tueda/formset/1.0.0/formset/formset.py) manually.\n\n\nUsage\n-----\n\n```shell\nformset     # prints a set of adequate setup parameters\n\nformset -o  # writes a set of adequate setup parameters to "form.set"\n```\n\nNote that this script considers only *static* buffers, allocated\nat the start-up of FORM.\nIf your FORM program uses much bigger *dynamical* buffers than usual\n(for example, you need to handle complicated rational functions\nor you want to optimize very huge polynomials)\nthen you need to adjust the initial memory usage by\nthe `--percentage N` (or `-p N`) option:\n\n```shell\nformset -p 50\n```\n\nIf your program requires a non-default `MaxTermSize` (or other parameters),\nthen you need to specify it:\n\n```shell\nformset MaxTermSize=200K\n```\n\nOther command-line options can be found in the help message:\n\n```shell\nformset --help\n```\n\n\n## License\n\n[MIT](https://github.com/tueda/formset/blob/main/LICENSE)\n',
    'author': 'Takahiro Ueda',
    'author_email': 'tueda@st.seikei.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tueda/formset',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*',
}


setup(**setup_kwargs)
