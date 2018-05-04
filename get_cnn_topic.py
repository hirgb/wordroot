#!/usr/bin/python3
# coding:utf-8

from mytool import *
from bs4 import BeautifulSoup
import json, db, re, pymysql


content = get_content('https://edition.cnn.com/data/ocs/section/index.html:intl_homepage1-zone-1/views/zones/common/zone-manager.izl', 'edition.cnn.com')
htmlstr = json.loads(content)['html']
url = re.search('<a href=\".*\" class=\"link-banner\"', htmlstr, re.I).group()
img = re.search('data-src-full16x9=\".*\"', htmlstr, re.I).group()

target_url = 'https://edition.cnn.com' + url[url.find('"')+1:url.find('" ')]
target_img = 'https:' + img[img.find('"')+1:img.find('" ')]

url = target_url
image = target_img

content = get_content(target_url, 'edition.cnn.com', 'utf-8')
soup = BeautifulSoup(content, 'lxml')

title = soup.h1.get_text().lstrip().rstrip()

query = "select count(*) from wordroot_cnn where title = '{title}'".format(title=title)
cursor = db.sqlquery(query)
count = cursor.fetchone()[0]

if count == 0:
    content = ''
    for i in soup.select('.zn-body__paragraph'):
        if i.get_text() != '':
            str = i.get_text()
            str = str.lstrip()
            str = str.rstrip()
            str = str.lstrip('(CNN)')
            if str.find('.') == -1:
                content += '<h4>' + str + '</h4>'
            else:
                content += '<p>' + str + '</p>'
    query = "insert ignore into wordroot_cnn (title, content, url, image) values (%s, %s, %s, %s)"
    con = pymysql.connect('localhost', 'root', '!QAZ2wsx', 'wavelab', charset='utf8')
    cursor = con.cursor()
    cursor.execute(query, (title, content, url, image))
    con.commit()
    con.close()
    log('get', '[%s] is added.' % title)
else:
    log('get', '[%s] is exist.' % title)
