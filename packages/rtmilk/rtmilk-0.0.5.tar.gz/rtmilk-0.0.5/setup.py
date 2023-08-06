# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rtmilk']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1', 'requests>=2.23.0']

setup_kwargs = {
    'name': 'rtmilk',
    'version': '0.0.5',
    'description': 'RTM API wrapper',
    'long_description': '# rtmilk\nPython wrapper for "Remember the Milk" [API](https://www.rememberthemilk.com/services/api/)\n\n# Usage\n```python\nfrom rtmmilk import API, FileStorage, RTMError\n\nstorage = FileStorage(\'rtm-token.json\')\napi = API(API_KEY, SHARED_SECRET, storage)\n\ntimeline = api.TasksCreateTimeline().timeline\ntry:\n    api.TasksAdd(timeline, \'task name\')\nexcept RTMError as e:\n    print(e)\n```\n\n# Authorization\n```python\nfrom rtmmilk import API, AuthorizationSession, FileStorage\n\napi = API(API_KEY, SHARED_SECRET, FileStorage(\'rtm-token.json\'))\nauthenticationSession = AuthorizationSession(api, \'delete\')\ninput(f"Go to {authenticationSession.url} and authorize. Then Press ENTER")\ntoken = authenticationSession.Done()\nprint(\'Authorization token written to rtm-token.json\')\n```\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/rtmilk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
