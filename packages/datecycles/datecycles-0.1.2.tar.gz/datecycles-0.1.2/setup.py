# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datecycles']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.1,<2.0.0', 'holidays>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'datecycles',
    'version': '0.1.2',
    'description': 'Simple library for complicated date cycling rules',
    'long_description': '# datecycles\n\nSimple library for complicated date cycling rules\n\n[PyPI](https://pypi.org/project/datecycles/)\n\n[GitHub](https://github.com/b10011/datecycles)\n\n## Installation\n\n```bash\npip install --upgrade datecycles\n```\n\n## "Documentation"\n\nCurrently there is no proper documentation, but the code is somewhat commented,\nthere are examples at the end of this README, there are bunch of tests and\nhere\'s explanations for the parameters:\n\n```python3\ndatecycles(\n    every_n,\n    unit,\n    day=None,\n    weekday=None,\n    start=None,\n    end=None,\n    count=None,\n    shift_to_workday=None,\n    country=None,\n    holidays=None,\n    tzinfo=None,\n)\n```\n\n`every_n: int` defines the cycle interval.\n\n`unit: str` defines the interval unit / cycle duration. Allowed values:\n`"day", "week", "month", "year"`.\n\n`day: Optional[int]` defines the day of month that is requested. Cannot be used\nwith `weekday`.\n\n`start: Optional[arrow.arrow.Arrow]` defines the minimum date.\n\n`end: Optional[arrow.arrow.Arrow]` defines the maximum date. Can be used with\n`count`.\n\n`count: Optional[int]` defines maximum number of results returned. Can be used\nwith `end`.\n\n`shift_to_workday: Optional[str]` defines how to handle results that are at\nweekends or holidays. `"next"` finds the next workday, `"previous"` finds the\nprevious workday, `"skip"` skips the result completely, `None` returns the\nresult as is without shifting the date.\n\n`country: str` defines the country to be used for holidays. Allowed values\nare those that can be found in Python\n[holidays](https://github.com/dr-prodigy/python-holidays) library. For example,\n`holidays.Finland` and `holidays.FI` both exist so values `"Finland"` and `"FI"`\nare both valid values.\n\n`holidays: Union[dict, list]` defines the holidays. Can\'t be used with\n`country`. If some custom holidays must be combined with country\'s holidays,\nsee [holidays](https://github.com/dr-prodigy/python-holidays) documentation\nregarding adding custom holidays.\n\n`tzinfo: str` defines the timezone used in results. `start` and `end` must also\nhave the same timezone that\'s defined here. Allowed values are those that\n[arrow](https://github.com/arrow-py/arrow) accepts as a timezone.\n\n## Usage\n\nImporting:\n\n```python3\n# Import the function\nfrom datecycles import datecycles\n```\n\n### Example 1\n\nCycle every month on 2nd day, starting from 2021-07-10, take 5 first results\n\n```python3\ndatecycles(\n    1,\n    "month",\n    day=2,\n    start=arrow.get(2021, 7, 10),\n    count=5\n)\n\n# [<Arrow [2021-08-02T00:00:00+00:00]>,\n#  <Arrow [2021-09-02T00:00:00+00:00]>,\n#  <Arrow [2021-10-02T00:00:00+00:00]>,\n#  <Arrow [2021-11-02T00:00:00+00:00]>,\n#  <Arrow [2021-12-02T00:00:00+00:00]>]\n```\n\n### Example 2\n\nCycle every month on first friday, starting from 2021-07-10 until end of year\n\n```python3\ndatecycles(\n    1,\n    "month",\n    weekday=(0, False, "friday"),\n    start=arrow.get(2021, 7, 10),\n    end=arrow.get(2021, 12, 31)\n)\n\n# [<Arrow [2021-08-06T00:00:00+00:00]>,\n#  <Arrow [2021-09-03T00:00:00+00:00]>,\n#  <Arrow [2021-10-01T00:00:00+00:00]>,\n#  <Arrow [2021-11-05T00:00:00+00:00]>,\n#  <Arrow [2021-12-03T00:00:00+00:00]>]\n```\n\n### Example 3\n\nCycle every month on first friday that appears in a full week, starting from\n2021-07-10 until end of year\n\n```python3\ndatecycles(\n    1,\n    "month",\n    weekday=(0, True, "friday"),\n    start=arrow.get(2021, 7, 10),\n    end=arrow.get(2021, 12, 31)\n)\n\n# [<Arrow [2021-08-06T00:00:00+00:00]>,\n#  <Arrow [2021-09-10T00:00:00+00:00]>,\n#  <Arrow [2021-10-08T00:00:00+00:00]>,\n#  <Arrow [2021-11-05T00:00:00+00:00]>,\n#  <Arrow [2021-12-10T00:00:00+00:00]>]\n```\n\n### Example 4\n\nCycle every 3rd month on last friday that appears in a full week, starting from\n2021-09-01, take 4 first results\n\n```python3\ndatecycles(\n    3,\n    "month",\n    weekday=(-1, True, "friday"),\n    start=arrow.get(2021, 9, 1),\n    count=4\n)\n\n# [<Arrow [2021-09-24T00:00:00+00:00]>,\n#  <Arrow [2021-12-24T00:00:00+00:00]>,\n#  <Arrow [2022-03-25T00:00:00+00:00]>,\n#  <Arrow [2022-06-24T00:00:00+00:00]>]\n```\n\n### Example 5\n\nCycle every 3rd month on last friday that appears in a full week, starting from\n2021-09-01, take 4 first results, in case the result is a weekend day or\nholiday in Finland, go to the next workday\n\n```python3\ndatecycles(\n    3,\n    "month",\n    weekday=(-1, True, "friday"),\n    start=arrow.get(2021, 9, 1),\n    count=4,\n    shift_to_workday="next",\n    country="Finland"\n)\n\n# [<Arrow [2021-09-24T00:00:00+00:00]>,\n#  <Arrow [2021-12-27T00:00:00+00:00]>,\n#  <Arrow [2022-03-25T00:00:00+00:00]>,\n#  <Arrow [2022-06-27T00:00:00+00:00]>]\n```\n',
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b10011/datecycles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
