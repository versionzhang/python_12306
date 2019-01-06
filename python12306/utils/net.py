import xml.etree.ElementTree as ET
import requests

from utils.log import Log


class ResponseError(Exception):
    pass


class ResponseCodeError(Exception):
    pass


def send_captcha_requests(session, urlmapping_obj, params=None, data=None, **kwargs):
    """
    xml data example:
        <HashMap>
        <result_message>验证码校验失败,信息为空</result_message>
        <result_code>8</result_code>
        </HashMap>
        format result data.
    """
    session.headers.update(urlmapping_obj.headers)
    response = session.request(method=urlmapping_obj.method,
                               url=urlmapping_obj.url,
                               params=params,
                               data=data,
                               timeout=10,
                               # allow_redirects=False,
                               **kwargs)
    if response.status_code == requests.codes.ok:
        if 'xhtml+xml' in response.headers['Content-Type']:
            data = response.text
            root = ET.fromstring(data)
            message = root.find('result_message').text
            code = root.find('result_code').text
            return {"result_message": message, "result_code": code}
        elif 'json' in response.headers['Content-Type']:
            return response.json()
        else:
            raise ResponseError
    else:
        raise ResponseCodeError


def get_captcha_image(session, urlmapping_obj, params=None, data=None, **kwargs):
    """
    xml data example:
        <HashMap>
            <result_message>生成验证码成功</result_message>
            <result_code>0</result_code>
            <image>imagedata<image>
        </HashMap>
        format result data.
    """
    session.headers.update(urlmapping_obj.headers)
    response = session.request(method=urlmapping_obj.method,
                               url=urlmapping_obj.url,
                               params=params,
                               data=data,
                               timeout=10,
                               # allow_redirects=False,
                               **kwargs)
    if response.status_code == requests.codes.ok:
        if 'xhtml+xml' in response.headers['Content-Type']:
            data = response.text
            root = ET.fromstring(data)
            message = root.find('result_message').text
            code = root.find('result_code').text
            image = root.find('image').text
            return {"result_message": message, "code": code, 'image': image}
        elif 'json' in response.headers['Content-Type']:
            return response.json()
        else:
            raise ResponseError
    else:
        raise ResponseCodeError


def send_requests(session, urlmapping_obj, params=None, data=None, **kwargs):
    session.headers.update(urlmapping_obj.headers)
    try:
        response = session.request(method=urlmapping_obj.method,
                                   url=urlmapping_obj.url,
                                   params=params,
                                   data=data,
                                   timeout=10,
                                   # allow_redirects=False,
                                   **kwargs)
        if response.status_code == requests.codes.ok:
            if 'xhtml+xml' in response.headers['Content-Type']:
                data = response.text
                root = ET.fromstring(data)
                return {v.tag: v.text for v in root.getchildren()}
            if 'json' in response.headers['Content-Type']:
                return response.json()
            # other type
            return response.text
        else:
            Log.w(response.url)
            Log.w(response.status_code)
    except Exception as e:
        Log.e(e)
    return None


def json_status(json_response, check_column, ok_code=0):
    """
    :param ok_code: ok code.
    :param json_response: json_response
    :param check_column: check column, add column missing message
    :return:
    """
    status = json_response.get('result_code', None) == ok_code
    if status:
        return status, "OK"
    else:
        return status, " ".join(["{column} not found".format(
            column=v
        ) for v in check_column if v not in json_response])
