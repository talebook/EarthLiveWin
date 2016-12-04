#! python2
# -*- coding: utf8 -*-

import re
import urllib2
import time
import json
import os
import logging
import datetime
import Tkinter
import tkMessageBox
import threading
import ctypes

__author__ = 'lniwn'
__mail__ = 'lniwn@live.com'


def set_wallpaper(picpath):
    done = ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, ctypes.create_unicode_buffer(picpath), 1)
    logging.info('set wallpaper %s' % ('successfully' if done else 'failed') )

def get_day():
    url = 'http://himawari8.nict.go.jp/himawari8/img/D531106/latest.json'
    url = 'http://hk.talebook.org/himawari8/img/D531106/latest.json'
    logging.debug(url)
    text = urllib2.urlopen(url).read()
    rsp = json.loads(text)
    try:
        return datetime.datetime.strptime(rsp['date'], "%Y-%m-%d %H:%M:%S")
    except:
        return None

def download(urls):
    for url in urls:
        logging.debug(url)
        try: return urllib2.urlopen(url).read()
        except Exception as e:
            logging.error(e)
    return None

def download_img(day):
    if not day: return None
    name = day.strftime("%Y/%m/%d/%H%M%S_0_0.png")
    urls = [
            "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/" + name,
            "http://hk.talebook.org/himawari8/img/D531106/1d/550/" + name,
            ]
    data_img = download(urls)
    picname = os.path.join(os.getcwd(), "Earth.png")
    if data_img:
        logging.info('Download newest image successfully.')
        with open(picname, 'wb') as fp:
            fp.write(data_img)

    if 'Earth.png' not in os.listdir(os.getcwd()):
        return None
    return picname

def main():
    interval = 60*10
    while True:
        picname = download_img(get_day())
        if picname: set_wallpaper(picname)
        time.sleep(interval)

if __name__ == '__main__':
    logging.basicConfig(
            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename="debug.log",
            level=logging.DEBUG)
    threading.Thread(target=main).start()
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo( "Earth Live", "EarthLive程序正在后台执行咯~")
    root.after(1, root.withdraw)
    root.mainloop()
