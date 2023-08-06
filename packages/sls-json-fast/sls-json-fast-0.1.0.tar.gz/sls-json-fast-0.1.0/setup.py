# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sls_json_fast']

package_data = \
{'': ['*']}

install_requires = \
['aliyun-log-python-sdk>=0.6.54,<0.7.0']

setup_kwargs = {
    'name': 'sls-json-fast',
    'version': '0.1.0',
    'description': 'aliyun sls log python for json',
    'long_description': '# 阿里云日志服务 for JSON\n\n## 使用\n\n- `ALIYUN_LOG_ENDPOINT` 日志服务端点，默认根据环境自动配置内外网\n- `ALIYUN_LOG_ACCESSID` 阿里云 access id\n- `ALIYUN_LOG_ACCESSKEY` 阿里云 access key\n- `ALIYUN_LOG_PROJECT` 阿里云日志项目名\n- `ALIYUN_LOG_STORE` 阿里云日志存储库名',
    'author': 'JimZhang',
    'author_email': 'zzl22100048@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
