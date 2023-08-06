# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rgov', 'rgov.commands']

package_data = \
{'': ['*'], 'rgov': ['data/*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'python-daemon>=2.3.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['rgov = rgov.application:main']}

setup_kwargs = {
    'name': 'rgov',
    'version': '0.2.3',
    'description': 'Check if campsites are available on Recreation.gov',
    'long_description': '\n# Table of Contents\n\n1.  [rgov - Recreation.gov Campground Checker](#orgef9b9d8)\n    1.  [Installation](#org9713277)\n    2.  [Quick Start](#org44d7cf0)\n    3.  [Commands](#orgb1d63b5)\n        1.  [Search](#org637d06c)\n        2.  [Check](#org3990b98)\n        3.  [Daemon](#orgaad63e2)\n        4.  [Reindex](#org9b91123)\n    4.  [Todo](#org3da19f3)\n\n\n<a id="orgef9b9d8"></a>\n\n# rgov - Recreation.gov Campground Checker\n\n[![img](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)\n\n`rgov` is a command line program to check for campground availability on\nRecreation.gov. While other recreation.gov scrapers exist, this one aims to\nalso provide a simple search command for quickly finding the campsite ids that\nare necessary for checking campgrounds. It also includes a daemon to check for\navailability automatically.\n\nIt is becoming increasingly more difficult to find campsites on Recreation.gov,\nso if you use this tool, please use it with discretion!\n\n\n<a id="org9713277"></a>\n\n## Installation\n\nRequires: Python 3.6+\n\nWith pip:\n\n$ `pip install rgov`\n\n\n<a id="org44d7cf0"></a>\n\n## Quick Start\n\nFirst, find your campgrounds id (usually a six-digit number):\n\n$ `rgov search <campground>`\n\nYou can also find the id in the url of the campgound\'s page on Recreation.gov.\n\nTo check if there are available sites (separate multiple ids with spaces):\n\n$ `rgov check <campground id(s)> --date <mm-dd-yyyy> --length <number of nights>`\n\nIf there aren\'t, you can run automated checks. Start the daemon with your\npreferred method of notification (either a notification program or your own\nshell command):\n\n$ `rgov daemon <campground id(s)> --date <...> --length <...> --command <your command>`\n\nThis will check every five minutes.\n\n\n<a id="orgb1d63b5"></a>\n\n## Commands\n\n\n<a id="org637d06c"></a>\n\n### Search\n\nSearch for campground ids for user with the `check` and `daemon` commands:\n\n$ `rgov search <search term(s)>`\n\nOnce you get the id, you can use that to check for availability.\n\nIf the index has been built with descriptions (see the reindex command),\nyou can search in the campground descriptions like this:\n\n$ `rgov search <search term(s)> --descriptions`\n\n\n<a id="org3990b98"></a>\n\n### Check\n\nThe check command quickly searches campgrouns for availability and prints which\nsites are available, if any.\n\n$ `rgov check <campground id(s)> -date <mm-dd-yyyy> -length <nights>`\n\n1.  Options\n\n    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">\n\n\n    <colgroup>\n    <col  class="org-left" />\n\n    <col  class="org-left" />\n    </colgroup>\n    <tbody>\n    <tr>\n    <td class="org-left"><code>--date[-d]</code></td>\n    <td class="org-left">The date to check (mm-dd-yyyy)</td>\n    </tr>\n\n\n    <tr>\n    <td class="org-left"><code>--length[-l]</code></td>\n    <td class="org-left">The number of days you\'ll be staying</td>\n    </tr>\n\n\n    <tr>\n    <td class="org-left"><code>--url[-u]</code></td>\n    <td class="org-left">Show the url of campground</td>\n    </tr>\n    </tbody>\n    </table>\n\n\n<a id="orgaad63e2"></a>\n\n### Daemon\n\nSimiliar to the `check` command, the `daemon` command starts a daemon that\nchecks for availability every five minutes in the background. The method of\nnotification is up to you, and can either be a notification program or custom\nshell command.\n\n$ `rgov daemon <campground id(s)> --date <mm-dd-yyyy> --length <nights> --notifier <notification program> --command <shell command>`\n\n1.  Options\n\n    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">\n\n\n    <colgroup>\n    <col  class="org-left" />\n\n    <col  class="org-left" />\n    </colgroup>\n    <tbody>\n    <tr>\n    <td class="org-left"><code>--date[-d]</code></td>\n    <td class="org-left">The date to check (mm-dd-yyyy)</td>\n    </tr>\n\n\n    <tr>\n    <td class="org-left"><code>--length[-l]</code></td>\n    <td class="org-left">The number of days you\'ll be staying</td>\n    </tr>\n\n\n    <tr>\n    <td class="org-left"><code>--notifier[-n]</code></td>\n    <td class="org-left">Specify a notification program to use (e.g. herbe)</td>\n    </tr>\n\n\n    <tr>\n    <td class="org-left"><code>--command[-c]</code></td>\n    <td class="org-left">The shell command to run if site(s) are found</td>\n    </tr>\n    </tbody>\n    </table>\n\n\n<a id="org9b91123"></a>\n\n### Reindex\n\nThis only needs to be run if you wish to search for campgrounds by description,\nwhich is useful for finding campground by city, region, or park name. It will\ndownload the facility data from recreation.gov, and build the index from that.\n\nYou can add the descriptions to the search index like this:\n\n$ `rgov reindex --with-descriptions`\n\nFor any reason, you can remove the descriptions with:\n\n$ `rgov reindex`\n\n\n<a id="org3da19f3"></a>\n\n## Todo\n\n[ ] Add additional ways for notifications to be sent (e.g. phone/email)\n\n[ ] Write more testing\n',
    'author': 'Jordan Sweet',
    'author_email': 'jsbmgcontact@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
