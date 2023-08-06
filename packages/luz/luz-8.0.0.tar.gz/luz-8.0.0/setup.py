# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['luz']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0', 'torch>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'luz',
    'version': '8.0.0',
    'description': 'Framework for rapid research and development of machine learning projects using PyTorch.',
    'long_description': "==============\nLuz Module\n==============\n\n.. image:: https://codecov.io/gh/kijanac/luz/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/kijanac/luz\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github\n\n**Framework for rapid research and development of machine learning projects using PyTorch.**\n\nLonger description coming soon!\n\nImportant features:\n\n#. Reduced boilerplate and simple specifications of complex workflows\n#. Easy and flexible customization of Learner by overriding methods\n#. Built-in scoring algorithms like holdout and cross validation\n#. Straightforward hyperparameter tuning with built-in tuning algorithms like random search and grid search\n\nBasic usage: custom modules with luz.Module functionality. Simply define your model, inherit from luz.Module, and use model.train/model.test.\n\nNext level: simplified training algorithms with transforms and handlers.\n\nNext level: straightforward hyperparameter tuning with various scoring mechanisms.\n\n#. Data preparation scheme.\n\n  #. Transforms: Functions for conditionining the training process which are invertible and whose inverse is applied to the resulting predictor.\n  #. Preprocessors: Functions for altering the prediction task which are not necessarily invertible.\n\n#. Model.\n#. Training scheme.\n#. Overall learning algorithm.\n\n  #. Hyperparameter selection.\n\n#. Unified development interface through Learner object. Simply inherit luz.Learner, define the model, loader, and param functions, and you're good to go. Add a hyperparams function to enable tuning and make tuned parameters accessible in the model and param functions.\n\n---------------\nGetting Started\n---------------\n\nPrerequisites\n-------------\n\nInstalling\n----------\n\nTo install, open a shell terminal and run::\n\n`conda create -n luz -c conda-forge -c pytorch -c kijana luz`\n\n----------\nVersioning\n----------\n\n-------\nAuthors\n-------\n\nKi-Jana Carter\n\n-------\nLicense\n-------\nThis project is licensed under the MIT License - see the LICENSE file for details.\n",
    'author': 'Ki-Jana Carter',
    'author_email': 'kijana@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kijanac/luz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
