#!/usr/bin/env python
# coding: utf-8

import urllib2
import httplib

NO_SUCH_HOST = "[Errno -2] Name or service not known" # нет такого адреса или вообще инета

class URLError(Exception):
    """ Комбинированное искючение (URLError, HTTPError) в случае проблем с соединением """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'parse_html.URLError: %s' % self.msg

def urlerror_to_message(msg):
    res = msg

    dict = { NO_SUCH_HOST: "Недоступен интернет-адрес", "404": "Нет такого адреса, 404" }
    if msg in dict.keys():
        res = dict[msg]

    return res

def get_url(url, data=None):
    """ 
    Возвращает открытый файловый объект
    Запускает исключение parse_html.URLError в случае ошибки"""
    
    res = True
    msg = ''
    try:
        f = urllib2.urlopen(url, data)
    except urllib2.HTTPError, err:
        res = False
        msg = str(err.code) # 404, ...
    except urllib2.URLError, err:
        res = False
        # reason это socket.error (gaierror) класс, у которого 
        # при желании можно выцепить атрибуты errno, string
        msg = str(err.reason)
    except httplib.BadStatusLine, err:
        res = False
        msg = "Сервер плохо ответил на GET-запрос: '%s'" % err.line

    if not res:
        raise URLError(msg)

    return f

def get_http_url(server_path, get_path):
    """ 
    Вариант с использованием httplib напрямую; ничем не лучше urllib2
    server_path = "example.com"
    get_path    = "/some_path"
    """

    # urllib - более высокого уровня библиотека, которая в случае http использует
    # httplib;
    # используем httplib ради лучшего детектирования ошибок
    direct_http = 1

    if direct_http:
        import httplib
        conn = httplib.HTTPConnection(server_path)
        try:
            conn.request("GET", get_path)
        except:
            raise RuntimeError("Cant connect to: " + server_path)
        response = conn.getresponse()

        if response.reason != 'OK':
            raise RuntimeError("Error getting data from: " + get_path)
        #print response.status, response.reason, response.msg
        return response
    else:
        import urllib
        f = urllib.urlopen("http://" + server_path + get_path)
        #print f.info()

        return f

###################

# считаем эталоном Рунета
etalon_url = "http://ya.ru/"

def test_inet(url=etalon_url):
    res = True
    msg = ''
    try:
        f = get_url(url)
        f.close()
    except URLError, err:
        res = False
        msg = err.msg
    return res, msg

