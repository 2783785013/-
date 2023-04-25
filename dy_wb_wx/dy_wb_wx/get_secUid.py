import requests
import re
from settings import *
import time

def get_proxies():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxies_info_request['proxyHost'],
        "port": proxies_info_request['proxyPort'],
        "user": proxies_info_request['proxyUser'],
        "pass": proxies_info_request['proxyPass'],
    }
    return {"http": proxyMeta, "https": proxyMeta}


# @retry(Exception, tries=5, delay=5, backoff=2, max_delay=20, )
def send_requests(url, headers=None, params=None, data=None, allow_redirects=False, retry=0):
    Session = requests.session()
    if retry < 5:
        proxies = get_proxies()
        headers = headers if headers else headers
        try:
            if data:
                response = Session.post(url, headers=headers, params=params, data=data, proxies=proxies,
                                             allow_redirects=allow_redirects)
            else:
                response = Session.get(url, headers=headers, params=params, proxies=proxies,
                                            allow_redirects=allow_redirects)
        except Exception as e:
            # print('send_requests ->：', e)
            time.sleep(5)
            retry += 1
            return send_requests(url, headers=headers, params=params, data=data, retry=retry)
        else:
            return response
    return None


def get_secUid(FalseLink):
    # print(FalseLink)
    response = send_requests(FalseLink, allow_redirects=False)
    if response:
        try:
            if response.headers.get('Location'):
                link = response.headers.get('Location')
                link_ = re.findall(r'sec_uid\=(.*?)\&',link)[0]
                # print(link_)
                return link_
        except Exception as e:
            print(e)
    return None

if __name__ == '__main__':
    # get_secUid('https://v.douyin.com/eMoogQu/')
    print(get_proxies())

