# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['siftlog', 'siftlog.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'siftlog-py',
    'version': '0.9.2',
    'description': 'Structured JSON logging',
    'long_description': 'Sift Log - JSON logging adapter for Python (now in color)\n===============\n\n## Features\n* Tag log statements with arbitrary values for easier grouping and analysis\n* Add keyword arguments that are converted to JSON values\n* Variable substitution\n* Specifies where log calls are made from\n* Meant to be used with core Python logging (formatters, handlers, etc)\n* Colorized logs on a console (POSIX only)\n* `TRACE` log level built-in\n \n## Examples\n#### A simple log message\n```python\nlog.info(\'Hello\')\n```\n`{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO", "loc": "test:log_test:20"}`\n\n#### Logging with tags\n```python\nlog.debug(\'Creating new user\', \'MONGO\', \'STORAGE\')\n```\n`{"msg": "Creating new user", "time": "12-12-14 10:12:09 EST", "tags": ["MONGO", "STORAGE"], "level": "DEBUG", "loc": "test:log_test:20"}`\n\n#### Appending more data\n```python\nlog.debug(\'Some key\', is_admin=True, username=\'papito\')\n```\n`{"msg": "Some key", "is_admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG", "loc": "test:log_test:20"}`\n\n#### String substitution\n```python\nlog.debug(\'User "$username" admin? $is_admin\', is_admin=False, username=\'fez\')\n```\n`{"msg": "User \\"fez\\" admin? False",  "username": "fez", "is_admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG", "loc": "test:log_test:20"}`\n\n\n## Setup\n#### Logging to console\n```python\nimport sys\nimport logging\nfrom siftlog import SiftLog\n\nlogger = logging.getLogger()\nlogger.setLevel(logging.INFO)\nhandler = logging.StreamHandler(sys.stdout)\nlogger.addHandler(handler)\n\nlog = SiftLog(logger)\n```\nIn this fashion, you can direct the JSON logs to [any logging handler](https://docs.python.org/2/library/logging.handlers.html)\n\n#### Color\nFor enhanced flamboyancy, attach the `ColorStreamHandler` to your logger. The output will not have color if the logs\nare being output to a file, or on systems that are not POSIX (will not work on Windows for now).\n\n```python\nfrom siftlog import SiftLog, ColorStreamHandler\n\nlogger = logging.getLogger()\nhandler = ColorStreamHandler(sys.stdout)\nlogger.addHandler(handler)\n\nlog = SiftLog(logger)\n```\n\n##### Performance\n\nWhile the above should play, it\'s highly recommended that the color handler is only \nattached conditionally for local development. Too many log statements could otherwise become\nexpensive in terms of CPU.\n\n\n##### Different colors\nYou can change font background, text color, and boldness:\n\n```python\nfrom siftlog import ColorStreamHandler\n\nhandler = ColorStreamHandler(sys.stdout)\nhandler.set_color(\n    logging.DEBUG, bg=handler.WHITE, fg=handler.BLUE, bold=True\n)\n```\n\n##### Supported colors\n * ColorStreamHandler.BLACK\n * ColorStreamHandler.RED\n * ColorStreamHandler.GREEN\n * ColorStreamHandler.YELLOW\n * ColorStreamHandler.BLUE\n * ColorStreamHandler.MAGENTA\n * ColorStreamHandler.CYAN\n * ColorStreamHandler.WHITE\n\n#### Constants (re-occuring values)\nYou can define constants that will appear in every single log message. This is useful, for example, if you\'d like to log process PID and hostname with every log message (recommended). This is done upon log adapter initialization:\n\n```python\nimport os\nfrom siftlog import SiftLog\nlog = SiftLog(logger, pid=os.getpid(), env=\'INTEGRATION\')\n```\n`{"msg": "And here I am", "time": "12-12-14 11:12:24 EST", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}`\n\n\n#### Custom time format\n```python\nlog = SiftLog(logger)\nSiftLog.TIME_FORMAT = \'%d-%m-%y %H:%m:%S %Z\'\n```\nDefine the format as accepted by [time.strftime()](https://docs.python.org/2/library/time.html#time.strftime)\n\n#### Custom location format\n```python\nlog = SiftLog(logger)\nSiftLog.LOCATION_FORMAT = \'$module:$method:$line_no\'\n```\nThe format should be a string containing any of the following variables:\n\n * `$file`\n * `$line_no`\n * `$method`\n * `$module`\n\n#### Custom core key names\nCore keys, such as `msg` and `level` can be overridden, if they clash with common keys you might be using.\n\nThe following can be redefined:\n\n * SiftLog.MESSAGE (default `msg`)\n * SiftLog.LEVEL (default `level`)\n * SiftLog.LOCATION (default `loc`)\n * SiftLog.TAGS (default `tags`)\n * SiftLog.TIME (default `time`)\n\nAs in:\n\n```python\nlog = SiftLog(logger)\nSiftLog.log.MESSAGE = "MESSAGE"\n```\n\n## Development flow\n\n`Poetry` is used to manage the dependencies.\n\nMost things can be accessed via the Makefile, if you have Make installed.\n\n    # use the right Python\n    poetry use path/to/python/3.8-ish\n    # make sure correct Python is used\n    make info\n    # install dependencies\n    make install\n    # run tests\n    make test\n    # formatting, linting, and type checking\n    make lint\n',
    'author': 'Andrei Taranchenko',
    'author_email': 'drey10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/papito/siftlog-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
