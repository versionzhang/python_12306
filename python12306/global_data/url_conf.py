# copy url config from easytrain repo.
import random
import time

from python12306.utils.data_structure import UrlMapping

LOGIN_URLS = {
    'normal': {
        'init1':
            {
                'url': r'https://kyfw.12306.cn/',
                'method': 'GET',
                'headers': {
                    'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                },
                'response': 'html',
            },
        'init2':
            {
                'url': r'https://kyfw.12306.cn/otn/',
                'method': 'GET',
                'headers': {
                    'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                },
                'response': 'html',
            },
        'init3':
            {
                'url': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/',
                'method': 'GET',
                'headers': {
                    'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                },
                'response': 'html',
            },
        'init': {
            'url': r'https://kyfw.12306.cn/otn/resources/login.html',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
        'init4': {
            'url': r'https://kyfw.12306.cn/otn/login/conf',
            'method': 'POST',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': r'https://kyfw.12306.cn/otn/resources/login.html',
            }
        },
        'init5': {
            'url': r'https://kyfw.12306.cn/otn/index12306/getLoginBanner',
            'method': 'GET',
            'headers': {
                'Accept': r'text/plain, */*; q=0.01',
                'Referer': r'https://kyfw.12306.cn/otn/resources/login.html',
            }
        },
        'init6': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk-static',
            'method': 'POST',
            'headers': {
                'Accept': r'*/*',
                'Referer': r'https://kyfw.12306.cn/otn/resources/login.html',
            }
        },
        'init7': {
            'url': r'https://kyfw.12306.cn/passport/web/create-qr64',
            'method': 'POST',
            'headers': {
                'Accept': r'*/*',
                'Referer': r'https://kyfw.12306.cn/otn/resources/login.html',
            }
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            },
            'response': 'html'
        },
        'captcha': {
            # use lambda function, every time to generator a different number.
            # change this link, because of web change this interface.
            'url': lambda: r'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&{}'.format(
                int(time.time() * 1000)
            ),
            'method': 'GET',
            'response': 'json'
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/passport/captcha/captcha-check',
            # 2019.03.28 use post method.
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/resources/login.html',
            },
            'response': 'json'
        },
        'login': {
            'url': r'https://kyfw.12306.cn/passport/web/login',
            'method': 'POST',
            'headers': {
                'X-Requested-With': 'xmlHttpRequest',
                'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            }
        },
        'userLogin': {
            'url': r'https://kyfw.12306.cn/otn/login/userLogin',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            },
            'response': 'html',
        },
        'userLoginRedirect': {
            'url': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'method': 'GET',
            'response': 'html',
        },
        'uamauthclient': {
            'url': r'https://kyfw.12306.cn/otn/uamauthclient',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'checkUser': {
            'url': r'https://kyfw.12306.cn/otn/login/checkUser',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'logout': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            },
            'response': 'html',
        },
    },
    # --------------------------------------------------------------------------------------------------------
    'other': {
        'init': {
            'url': r'https://kyfw.12306.cn/otn/resources/login.html',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'captcha': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&rand=sjrand&{}'
                .format(random.random()),
            'method': 'GET',
            'response': 'binary',
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
            'method': 'POST',
            'headers': {
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init'
            }
        },
        'login': {
            'url': r'https://kyfw.12306.cn/otn/login/loginAysnSuggest',
            'method': 'POST',
            'headers': {
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'logout': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                'Host': r'kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
    },
}

QUERY_URL = {
    'url': r'https://kyfw.12306.cn/otn/leftTicket/query',
    'method': 'GET',
    'headers': {
        'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init'
    },
    'type': 'cdn'
}

SUBMIT_URLS = {
    'dc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Host': r'kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
            'response': 'json'
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
            },
            'response': 'json'
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
            },
            'response': 'json'
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'queryMyOrderNoComplete': {
            'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
            },
        }

    },
    'wc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmGoForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc'
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'queryMyOrderNoComplete': {
            'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
            },
        }

    }
}

FAST_SUBMIT_URLS = {
    'autoSubmitOrderRequest': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/autoSubmitOrderRequest',
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        },
    },
    "getQueueCountAsync": {  # 快速获取订单数据
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCountAsync",
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        },
    },
    "confirmSingleForQueueAsys": {  # 快速订单排队
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueueAsys",
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        },
    },
    'getExtraInfo': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        'method': 'GET',
        'response': 'html',
    },
    'getPassengerDTOs': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
        'method': 'POST',
    },
    'queryOrderWaitTime': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
        'method': 'GET',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
        },
    },
    'resultOrderForQueue': {
        'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue',
        'method': 'POST',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
        },
    },
}

PASSENGER_URL = {
    'url': r'https://kyfw.12306.cn/otn/passengers/query',
    'method': 'POST',
    'headers': {
        'Referer': r'https://kyfw.12306.cn/otn/view/passengers.html',
    }
}

USER_CHECK_URL = {
    'url': r'https://kyfw.12306.cn/otn/login/checkUser',
    'method': 'POST',
    'headers': {
        'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
    }
}

ORDER_NO_COMPLETE_URL = {
    'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
    'method': 'POST',
    'headers': {
        'Referer': r'https://kyfw.12306.cn/otn/view/train_order.html'
    }
}

DEVICE_FINGERPRINT_URL = {
    'url': r'https://kyfw.12306.cn/otn/HttpZF/logdevice',
    'method': 'GET',
    'headers': {
        'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/'
    },
    'type': 'text'
}


USER_CHECK_URL_MAPPING = UrlMapping(USER_CHECK_URL)
PASSENGER_URL_MAPPING = UrlMapping(PASSENGER_URL)
LOGIN_URL_MAPPING = {key: {key1: UrlMapping(v1) for key1, v1 in v.items()} for key, v in LOGIN_URLS.items()}
QUERY_URL_MAPPING = UrlMapping(QUERY_URL)
DEVICE_FINGERPRINT_MAPPING = UrlMapping(DEVICE_FINGERPRINT_URL)
SUBMIT_URL_MAPPING = {key: {key1: UrlMapping(v1) for key1, v1 in v.items()} for key, v in SUBMIT_URLS.items()}
FAST_SUBMIT_URL_MAPPING = {key: UrlMapping(v) for key, v in FAST_SUBMIT_URLS.items()}
ORDER_NO_COMPLETE_MAPPING = UrlMapping(ORDER_NO_COMPLETE_URL)
