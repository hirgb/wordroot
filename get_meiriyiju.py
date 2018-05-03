#!/usr/bin/python3
# coding:utf-8

from urllib import request
import json, db

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

query = "insert ignore into wordroot_mryj (date, data) values ('{date}', '{data}')"\
    .format(date=content['dateline'], data=dict_str)
db.sqlquery(query)
