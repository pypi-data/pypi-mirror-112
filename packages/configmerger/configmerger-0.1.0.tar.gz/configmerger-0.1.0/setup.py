# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['configmerger']
setup_kwargs = {
    'name': 'configmerger',
    'version': '0.1.0',
    'description': 'merge multi level configurations',
    'long_description': "# configmerger\n\nmerge multi level configurations.\n\n## Usage\n\n``` py\nfrom configmerger import Merger\n\n# your configurations, read from app.json, machine.yaml, user.toml, or more\nconfs = [\n    read_from_app(),\n    read_from_machine(),\n    read_from_user(),\n]\n\n# merge all configurations into one.\nruntime_conf = Merger().merge(confs)\n```\n\n## Merge Rules\n\nHere is the default merge rules:\n\n``` py\nmerger = Merger()\n\n# for dict, a little like Chainmap\nmerger.merge([\n    {'a': 1},\n    {'a': 2, 'b': 3},\n    {        'b': 4}\n])\n#   {'a': 2, 'b': 4}\n\n# for list, default behavior is connect each\n# change `merger.connect_list` to `False` can change this behavior\nmerger.merge([ [1, 2, 3], [4, 5] ]) # [4, 5, 1, 2, 3]\n\n# for str, int and others, latest have highest priority\nmerger.merge([ 'first', 'last' ]) # 'last'\n\n# basic, `None` is ignored\nmerger.merge([ 1, None ]) # 1\n\n# but if all values is `None`, return `None`\nmerger.merge([ None, None ]) # None\n\n# if type changed, merge will stop,\nmerger.merge([\n    {'a': 1},   # <--- ignored\n    1,          # <--- type changed, ignore all before this\n    {'b': 2},\n    None,       # <--- None is ignored\n    {'c': 3},\n])# {'b': 2, 'c': 3}\n```\n\nOverride any methods to modify the default behavior.\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cologler/configmerger-python',
    'py_modules': modules,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
