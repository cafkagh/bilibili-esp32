# -*- coding: utf-8 -*-
import urllib2 as ul2
from Curl import Curl
import base64
import os
import random


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

    def get(self, url="127.0.0.1", path="./download", override=False, header=True):
        self.url = url
        self.path = path
        self.override = override
        self.filename = url.split("/")[-1]
        self.source = Curl(url=self.url)
        self.data = self.source.get()
        self.header = header
        return self

    def as_file(self):
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        except IOError as e:
            print(e)

        files = os.listdir(self.path)
        if (self.filename in files) and (self.override==False):
            file__name = self.filename.split(".")
            filename = file__name[0]+"-"+str(random.randint(100000, 999999))+"."+file__name[-1]
        else:
            filename = self.filename


        with open(self.path+"/"+filename, "wb") as f:
            f.write(self.data)
        f.close()
        return self.path+"/"+filename

    def as_base64(self):
        ext_name = self.filename.split(".")[-1]
        header = {
            "gif": "data: image/gif;base64,",
            "png": "data:image/png;base64,",
            "jpg": "data:image/jpeg;base64,",
            "ico": "data:image/x-icon;base64,"
        }
        base64_str = base64.b64encode(self.data).decode()
        if(self.header==True):
            base64_str = header[ext_name]+base64_str
        return base64_str


if __name__ == "__main__":
    download = Download()
    # print download.get(url="https://s1.bqiapp.com/image/20190620/6771561015029713.png", override=False).as_file()
    # print download.get(url="https://s1.bqiapp.com/image/20190620/6771561015029713.png").as_base64()
