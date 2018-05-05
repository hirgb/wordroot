#!/usr/bin/python3
# coding:utf-8

from urllib import request
from mytool import *
import json, pymysql


def get_content(url, host, encode):
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


content = json.loads(get_content('http://open.iciba.com/dsapi/', 'open.iciba.com', 'gbk'))
del content['love'], content['caption'], content['translation'], content['sp_pv'], \
    content['tags'], content['tts'], content['fenxiang_img'], content['s_pv'], \
    content['picture']

dict_str = json.dumps(content, ensure_ascii=False)

query = "insert ignore into wordroot_mryj (date, data) values (%s, %s)"

con = pymysql.connect('localhost', 'root', '!QAZ2wsx', 'wavelab', charset='utf8')
cursor = con.cursor()
cursor.execute(query, (content['dateline'], dict_str))
con.commit()
con.close()
log('get', 'meiriyiju is added.')
