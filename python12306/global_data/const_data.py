from python12306.utils.data_structure import TourMapping, SeatMapping, TicketMapping

TYPE_LOGIN_NORMAL_WAY = 0
TYPE_LOGIN_OTHER_WAY = 1

TOUR_DATA = [
    {
        "name": "单程",
        "sys_code": "dc"
    },
    {
        "name": "往返",
        "sys_code": "wc"
    }
]

SEAT_DATA = [
    {
        "name": '商务座',
        "sys_code": '9'
    },
    {
        "name": '特等座',
        "sys_code": 'P'
    },
    {
        "name": '一等座',
        "sys_code": 'M'
    },
    {
        "name": '二等座',
        "sys_code": 'O'
    },
    {
        "name": '高级软卧',
        "sys_code": '6'
    },
    {
        "name": '软卧',
        "sys_code": '4'
    },
    {
        "name": '硬卧',
        "sys_code": '3'
    },
    {
        "name": '软座',
        "sys_code": '2'
    },
    {
        "name": '硬座',
        "sys_code": '1'
    },
    {
        "name": '无座',
        "sys_code": '1'
    }
]

TICKET_DATA = [
    {
        "name": "成人票",
        "user_code": '1',
        "sys_code": "ADULT"
    },
    {
        "name": "儿童票",
        "user_code": '2',
        "sys_code": ""
    },
    {
        "name": "学生票",
        "user_code": '3',
        "sys_code": "0X00"
    },
    {
        "name": "残军票",
        "user_code": '4',
        "sys_code": ""
    }
]

SUBMIT_ERR_MESSAGES_LIST = [
    {"msg": "没有足够的票"},
    {"msg": "存在与本次购票行程冲突的车票"}
]

ORDER_NOT_FINISHED_MESSAGE = {"msg": "您还有未处理的订单"}

TourTypeList = [TourMapping(v) for v in TOUR_DATA]
SeatTypeList = [SeatMapping(v) for v in SEAT_DATA]
TicketTypeList = [TicketMapping(v) for v in TICKET_DATA]

FREE_CAPTCHA_URL = "https://12306.jiedanba.cn/api/v2/getCheck"
FREE_CAPTCHA_CHECK_URL = "https://check.huochepiao.360.cn/img_vcode"

FREE_CAPTCHA_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,en-US;q=0.9,zh;q=0.8,zh-CN;q=0.7",
    "Cache-Control": "max-age=0",
    "Content-Type": "text/plain",
    "Referer": "https://check.huochepiao.360.cn/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

DEVICE_FINGERPRINT = "algID=9VTu8J3Cya&hashCode=VLL9HVCtHYaBH6ezOfHwKYaVo6gPp3XKu-JVG06g29Y&FMQw=0&q4f3=zh-CN&VPIf=1&custID=133&VEek=unknown&dzuS=0&yD16=0&EOQP=fdab098ff58158f73d1f6a9052936019&lEnu=3232256537&jp76=52d67b2a5aa5e031084733d5006cc664&hAqN=Win32&platform=WEB&ks0Q=d22ca0b81584fbea62237b14bd04c866&TeRS=1040x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/73.0.3683.86%20Safari/537.36&E3gR=e03245ea4cc21cf9bd59da053b429fc6&timestamp=1553749743355"

def find_by_phrase(msg):
    data = list(filter(lambda x: msg in x["msg"], SUBMIT_ERR_MESSAGES_LIST))
    if data:
        return True, data[0]
    else:
        return False, None


def find_by_name(f_type, name):
    """
    :param f_type: "seat" "tour" "ticket"
    :param name:
    :return:
    """
    m = dict(seat=SeatTypeList, tour=TourTypeList, ticket=TicketTypeList)
    data = list(filter(lambda x: x.name == name, m[f_type]))
    if data:
        return data[0]
    else:
        return None


def find_by_names(f_type, names):
    """
    :param f_type: "seat" "tour" "ticket"
    :param names:
    :return:
    """
    m = dict(seat=SeatTypeList, tour=TourTypeList, ticket=TicketTypeList)
    # 更新排序按照传入的names的key值排序
    result = []
    for name in names:
        for v in m[f_type]:
            if v.name == name:
                result.append(v)
    return result
