import requests
from lxml import html
import time

__author__ = 'haotianyin'


def cached_url(url):
    import os
    filename = 'root.html'
    path = os.path.join('cached', filename)

    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    else:
        r = requests.get(url)
        print(r.content)
        print(path)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


def parse_url(url):
    # print(url[0:2])
    if url[0:2] == '//':
        # print(url)
        url =  'http://' + url[2:]
        return url
    elif url[0] == '/':
        url = 'http://m.sohu.com' + url
        return url
    elif url[0:4] == 'http':
        return url
    else:
        return 'http://m.sohu.com'


def log(*args, **kwargs):
    # time.time() 返回 unix time
    format = '%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def getListofHref(url):
    listOfhref = []
    page = cached_url(url)
    root = html.fromstring(page)
    list_a = root.xpath('//a')

    for element in list_a:
        href_url = element.xpath('.//@href')
        if len(href_url) != 0:
            # print(parse_url(href_url[0]))
            listOfhref.append(parse_url(href_url[0]))
    return listOfhref


def validDetect(listOfhref):
    log('Start')
    for e in listOfhref:
        # print(e)
        # log(e)
        try:
            print(e)
            r = requests.get(e, timeout=None)
            log(e, r.status_code)
        except:
            log('ERROR', e, r.status_code)
    log('Finished')


def main():
    url = 'http://m.sohu.com'

    # 得到页面内连接列表
    listOfhref = getListofHref(url)

    #有效性检测
    validDetect(listOfhref)


if __name__ == '__main__':
    main()
