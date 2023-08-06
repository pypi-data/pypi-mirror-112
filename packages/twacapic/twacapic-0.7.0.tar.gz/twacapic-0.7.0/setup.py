# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic', 'twacapic.templates']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'TwitterAPI>=2.6.9,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'schedule>=1.0.0,<2.0.0',
 'yagmail>=0.14.245,<0.15.0']

entry_points = \
{'console_scripts': ['twacapic = twacapic.main:run']}

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.7.0',
    'description': 'A Twitter Academic API Client',
    'long_description': '# twacapic\n\nTwitter Academic API Client\n\nIn development. Expect breaking changes and bugs when updating to the latest version.\n\nTested on Linux (Ubuntu 20.10, Python 3.8) and MacOS 11 (Python 3.9). Please [raise an issue](https://github.com/Leibniz-HBI/twacapic/issues) if you need to install it with another Python version or encounter issues with other operating systems.\n\n## Why another Twitter API client?\n\nIt is/will be more of a Twitter API client convenience wrapper that automates common tasks (e.g. get all tweets by a list of users and poll for new tweets regularly or get all tweets about an ongoing event based on keywords). That means, it actually makes use of existing API clients.\n\n## Installation\n\nConsider installlation via [pipx](https://pipxproject.github.io/pipx/) if you just want to use twacapic as a command line tool:\n\n1. If you like pipx, [install pipx](https://pipxproject.github.io/pipx/installation/)\n2. run `pipx install twacapic`\n\nOr, simply install via pip:\n\n`pip install twacapic` or `pip3 install twacapic`\n\n## Usage\n\n```txt\nusage: twacapic [-h] [-u [USERLIST ...]] [-g GROUPNAME [GROUPNAME ...]] [-c GROUP_CONFIG] [-l LOG_LEVEL] [-lf LOG_FILE]\n                [-s SCHEDULE] [-n NOTIFY]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u [USERLIST ...], --userlist [USERLIST ...]\n                        Path(s) to list(s) of user IDs, (format: one ID per line). Required for first run only. Same\n                        number and corresponding order required as in --groupname argument. Can be used to add users to\n                        a group.\n  -g GROUPNAME [GROUPNAME ...], --groupname GROUPNAME [GROUPNAME ...]\n                        Name(s) of the group(s) to collect. Results will be saved in folder `results/GROUPNAME/`. Can\n                        be used to poll for new tweets of a group. Default: "users"\n  -c GROUP_CONFIG, --group_config GROUP_CONFIG\n                        Path to a custom group config file to define tweet data to be retrieved, e.g. retweets,\n                        mentioned users, attachments. A template named `group_config.yaml` can be found in any already\n                        created group folder.\n  -l LOG_LEVEL, --log_level LOG_LEVEL\n                        Level of output detail (DEBUG, INFO, WARNING, ERROR). Warnings and Errors are always logged in\n                        respective log-files `errors.log` and `warnings.log`. Default: ERROR\n  -lf LOG_FILE, --log_file LOG_FILE\n                        Path to logfile. Defaults to standard output.\n  -s SCHEDULE, --schedule SCHEDULE\n                        If given, repeat every SCHEDULE minutes.\n  -n NOTIFY, --notify NOTIFY\n                        If given, notify email address in case of unexpected errors. Needs further setup. See README.\n```\n\nAt the moment twacapic can only collect the latest 100 tweets of a list of users and then poll for new tweets afterwards if called again with the same group name or if the `-s` argument is given.\n\nEmail notifications with the `-n` argument use the OAuth2 procedure of yagmail and necessitate an OAuth2 procedure to give access to a Gmail account as described in  its [README](https://github.com/kootenpv/yagmail#oauth2)\n\n### Authorisation with the Twitter API\n\nAt first use, it will prompt you for your API credentials, which you find [here](https://developer.twitter.com/en/portal/projects-and-apps). These credentials will be stored in a file in the working directory, so make sure that the directory is readable by you and authorised users only.\n\nFor non-interactive use, e.g. when automatically deploying twacapic to a server, this file can be used as a template and should always be placed in the working directory of twacapic.\n\n### Example\n\n`twacapic -g USER_GROUP_NAME -u PATH_TO_USER_CSV`\n\n`USER_GROUP_NAME` should be the name of the results folder that is meant to be created and will contain raw json responses from Twitter.\n\n`PATH_TO_USER_CSV` should be a path to a list of Twitter user IDs, without header, one line per user ID.\n\nAfterwards you can poll for new tweets of a user group by running simply:\n\n`twacapic -g USER_GROUP_NAME`\n\nEnjoy!\n\n### Config Template\n\nThe group config is a yaml file in the following form:\n\n```yaml\nfields:\n  attachments: No\n  author_id: Yes\n  context_annotations: No\n  conversation_id: No\n  created_at: No\n  entities: No\n  geo: No\n  in_reply_to_user_id: No\n  lang: No\n  non_public_metrics: No\n  organic_metrics: No\n  possibly_sensitive: No\n  promoted_metrics: No\n  public_metrics: No\n  referenced_tweets: No\n  reply_settings: No\n  source: No\n  withheld: No\nexpansions:\n  author_id: Yes\n  referenced_tweets.id: No\n  in_reply_to_user_id: No\n  attachments.media_keys: No\n  attachments.poll_ids: No\n  geo.place_id: No\n  entities.mentions.username: No\n  referenced_tweets.id.author_id: No\n```\n\nAn explanation of the fields and expansions can be found in Twitter\'s API docs:\n\n- [Fields](https://developer.twitter.com/en/docs/twitter-api/fields)\n- [Expansions](https://developer.twitter.com/en/docs/twitter-api/expansions)\n\n## Ensure that twacapic is continuously running, even after restart\n\nIf your system can run cronjobs, stop twacapic, run `crontab -e` and add the following to your crontab:\n\n```cron\n*/15 * * * *    cd PATH/TO/YOUR/TWACAPIC/WORKING/DIRECTORY && flock -n lock.file twacapic [YOUR ARGUMENTS HERE]\n```\n\nThis will check every 15 minutes whether twacapic is running (via the lock file), and if not, start it with your arguments.\n\n## Dev Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `twacapic` to enter API keys. Ignore the IndexError.\n6. Run `pytest` to run all tests\n',
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twacapic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
