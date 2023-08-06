import logging.config, os
import platform

__version__ = '0.1.0'


def __is_test_env():
    return os.environ.get('SPIDER_TEST', False) or platform.system() == "Windows"


def __get_endpoint():
    if __is_test_env():
        return "cn-shanghai.log.aliyuncs.com"
    else:
        return "cn-shanghai-intranet.log.aliyuncs.com"


conf = {'version': 1,
        'formatters': {'rawformatter': {'class': 'logging.Formatter',
                                        'format': '%(message)s'}
                       },
        'handlers': {'sls_handler': {'()':
                                         'aliyun.log.QueuedLogHandler',
                                     'level': 'INFO',
                                     'formatter': 'rawformatter',

                                     # custom args:
                                     'end_point': os.environ.get('ALIYUN_LOG_ENDPOINT', __get_endpoint()),
                                     'access_key_id': os.environ.get('ALIYUN_LOG_ACCESSID', ''),
                                     'access_key': os.environ.get('ALIYUN_LOG_ACCESSKEY', ''),
                                     'project': os.environ.get('ALIYUN_LOG_PROJECT', 'spider-test'),
                                     'log_store': os.environ.get('ALIYUN_LOG_STORE', "gs-log"),
                                     'extract_json': True,
                                     'extract_json_prefix': 'spider_',
                                     }
                     },
        'loggers': {'sls': {'handlers': ['sls_handler', ],
                            'level': 'INFO',
                            'propagate': False}
                    }
        }
logging.config.dictConfig(conf)


def get_logger():
    return logging.getLogger("sls")
