#!/usr/bin/python3
# coding:utf-8

from urllib import request
import datetime


def get_content(url, host='', encode='gbk'):
    """
    Get html content from url.
    :param url: <str>
    :param host: <str>
    :param encode: <str>
    :return: <json>
    """
    req = request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
    req.add_header("GET", url)
    req.add_header("Host", host)

    content_str = request.urlopen(req).read().decode(encode)
    return content_str


def log(status, message='', debugFlag=True):
    if debugFlag:
        print('{time} - {status} - {message}'.format(time=datetime.datetime.now(), status=status, message=message))
