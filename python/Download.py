# -*- coding: utf-8 -*-
import urllib2 as ul2
from Curl import Curl
import base64
import os
import random
import time


class Download:
    # 初始化
    def __init__(self):
        self.url = ''
        self.path = ''
        self.filename = ''
        self.source = ''
        self.data = ''
        self.override = ''
        self.header = ''

    def get(self, url="127.0.0.1", ):
        self.url = url
        self.source = Curl(url=self.url)
        self.data = self.source.get()
        return self

    def as_file(self, path="./download", filename="", data='', override=False):
        if filename == "":
            filename = self.url.split("/")[-1]
        else:
            filename = filename+"."+self.url.split("/")[-1].split(".")[-1]

        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except IOError as e:
            print(e)

        files = os.listdir(path)
        if (filename in files) and (override == False):
            file__name = filename.split(".")
            filename = file__name[0] + "-" + str(int(time.time())) +"-" + str(random.randint(1000, 9999)) + "." + file__name[-1]
        else:
            filename = filename

        if data == '':
            file_data = self.data
        else:
            file_data = data

        with open(path + "/" + filename, "wb") as f:
            f.write(file_data)
        f.close()
        # return path + "/" + filename
        return filename


    def as_base64(self, header=True):
        ext_name = self.filename.split(".")[-1]
        header = {
            "gif": "data: image/gif;base64,",
            "png": "data:image/png;base64,",
            "jpg": "data:image/jpeg;base64,",
            "ico": "data:image/x-icon;base64,"
        }
        base64_str = base64.b64encode(self.data).decode()
        if (header == True):
            base64_str = header[ext_name] + base64_str
        return base64_str


if __name__ == "__main__":
    download = Download()
    # print download.get(url="https://s1.bqiapp.com/image/20190620/6771561015029713.png", override=False).as_file()
    # print download.get(url="https://s1.bqiapp.com/image/20190620/6771561015029713.png").as_base64()
