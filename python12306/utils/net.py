import requests


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
            if urlmapping_obj.response == 'binary' and 'img' in response.headers['Content-Type']:
                return response.content
            if urlmapping_obj.response == 'html' and 'html' in response.headers['Content-Type']:
                response.encoding = response.apparent_encoding
                return response.text
            if urlmapping_obj.response == 'json' and 'json' in response.headers['Content-Type']:
                return response.json()
            # other type
            return response.text
        else:
            print(response.url)
            print(response.status_code)
    except Exception as e:
        print(e)
    return None


def json_status(json_response, check_column, ok_code=0):
    """
    :param ok_code: ok code.
    :param json_response: json_response
    :param check_column: check column, add column missing message
    :return:
    """
    if not isinstance(json_response, (dict, list)):
        return False, "can't parse data"
    status = json_response['result_code'] == ok_code if 'result_code' in json_response else False
    if status:
        return status, "OK"
    else:
        return status, " ".join(["{column} not found".format(
            column=v
        ) for v in check_column if v not in json_response])
