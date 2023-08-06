# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dask_lightgbm']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2.6.0,<3.0.0',
 'distributed>=2.6.0,<3.0.0',
 'lightgbm>=2.3.0,<3.0.0',
 'numpy>=1.17.3,<2.0.0',
 'toolz>=0.10.0,<0.11.0']

extras_require = \
{'sparse': ['sparse==0.5.0', 'scipy>=1.3.1,<2.0.0']}

setup_kwargs = {
    'name': 'dask-lightgbm',
    'version': '0.2.0',
    'description': 'LightGBM distributed training on Dask',
    'long_description': 'Dask-LightGBM - DEPRECATED\n==========================\n\nTHIS REPOSITORY IS DEPRECATED\n-----------------------------\n\nThis repository is deprecated and it is no longer maintained. The code was migrated into LightGBM package - https://github.com/microsoft/LightGBM.\n\n[![Build Status](https://github.com/dask/dask-lightgbm/workflows/CI/badge.svg)](https://github.com/dask/dask-lightgbm/actions?query=workflow%3ACI)\n\nDistributed training with LightGBM and Dask.distributed\n\nThis repository enables you to perform distributed training with LightGBM on\nDask.Array and Dask.DataFrame collections. It is based on dask-xgboost package.\n\nUsage\n-----\nLoad your data into distributed data-structure, which can be either Dask.Array or Dask.DataFrame.\nConnect to a Dask cluster using Dask.distributed.Client.\nLet dask-lightgbm train a model or make predictions for you.\nSee system tests for a sample code:\n<https://github.com/dask/dask-lightgbm/blob/main/system_tests/test_fit_predict.py>\n\nHow this works\n--------------\nDask is used mainly for accessing the cluster and managing data.\nThe library assures that both features and a label for each sample are located on the same worker.\nIt also lets each worker to know addresses and available ports of all other workers.\nThe distributed training is performed by LightGBM library itself using sockets.\nSee more details on distributed training in LightGBM here:\n<https://github.com/microsoft/LightGBM/blob/main/docs/Parallel-Learning-Guide.rst>\n',
    'author': 'Jan Stiborek',
    'author_email': 'honza.stiborek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dask/dask-lightgbm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
