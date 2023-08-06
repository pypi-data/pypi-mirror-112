# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mei2volpiano']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2021.1,<2022.0']

entry_points = \
{'console_scripts': ['mei2vol = mei2volpiano:driver.main',
                     'mei2volpiano = mei2volpiano:driver.main']}

setup_kwargs = {
    'name': 'mei2volpiano',
    'version': '0.8.2',
    'description': '',
    'long_description': '# MEI2Volpiano\nMEI2Volpiano is a Python library developed for the purpose of converting Neume and CWMN MEI files to Volpiano strings.\n\n## Licence\nMEI2Volpiano is released under the MIT license.\n\n## Installation\n\n* `pip install mei2volpiano`\n\n## Development Setup\n\nMEI2Volpiano requires at least Python 3.6.\n* Clone project `https://github.com/DDMAL/MEI2Volpiano.git`\n* Enter the project checkout\n* Execute `pip install .` or `poetry install` (this will install development dependencies)\n\n## Usage\n\nAs long as you\'re in the python environment, you can execute `mei2volpiano` or the shorthand `mei2vol` while in your python virtual environment\n\n### Flags\n\n| Flag        | Use           |\n| ------------- |:-------------:|\n| `-W` or `-N` | Used to specify the type of MEI to converted (Neume or CWN) |\n| `txt`| Used to specify whether the user is inputtng MEI files or a text file containing MEI paths |\n| `--export` | Signifies that the converted Volpiano string(s) should be outputted to \'.txt\' files    |\n\n### Standard Usage (Neume notation)\n\nTo output the MEI file\'s volpiano string to the terminal, run\n\n`mei2vol -N mei filename1.mei`\n\nMultiple files can be passed in at once\n\n`mei2vol -N mei filename1.mei filename2.mei`\n\n### Western\n\nTo convert MEI files written in Common Western Music Notation (CWMN), run\n\n`mei2vol -W mei filename1.mei`\n\nAll of the CWMN files processed by this library (so far) come from [this collection](https://github.com/DDMAL/Andrew-Hughes-Chant/tree/master/file_structure_text_file_MEI_file). Thus, we followed the conventions of those files. Namely:\n\n- Every neume is encoded as a quarter note\n- Stemless notes\n- Syllables are preceded by their notes\n- All notes must have syllables after them\n  * If there are notes that are not followed by a syllable, the script will display a message containing these notes. They will not be recorded in the volpiano\n  * This can only happen at the end of an MEI file \n\nThe resulting volpiano string will have multiple notes seperated by two hyphens. This seperation is dictated by the syllables, representented by: `<syl>`. The notes themselves are located with the `<note>` tag and represented by the `pname` attribute.\n\n### Mutiple MEI File Runs\n\nTo make it easier to pass in multiple MEI files, the `-t` flag can be specified as `txt`:\n\n`mei2vol -W txt filename1.txt` or `mei2vol -N txt filename1.txt filename2.txt ...`\n\nwhere the ".txt" file being passed in must hold the name/relative path of the required MEI files on distinct lines.\n\n**Note: If passing inputs through this method, the formats of the MEI files within the text file must be of the same type** (either neume for `-N` or western for `-W`)\n\n### Exporting\n\nThe `--export` tag can be used on any valid input to the program. Simply tack it on to the end of your command like so\n\n`mei2vol -N mei filename1.mei --export`\n\nand the program will output each mei file\'s volpiano to a similarly named file as its input.\n\n\n## Tests\n\nTo run the current test suite, execute `pytest`\n',
    'author': 'DDMAL',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DDMAL/MEI2Volpiano',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
