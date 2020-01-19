# -*- coding: utf-8 -*-
from __future__ import division, print_function
import time
import datetime
import random as rdm
import urllib2 as ul2
import json as js
import math
from Curl import Curl
from Pdo import Pdo as pdo
import sys
reload(sys)
sys.setdefaultencoding('utf8')

curl = Curl()
conn = pdo(dbtype="sqlite3", database="bilibili.db")


class Bilibili:
    # 初始化
    def __init__(self, mid):
        self.mid = mid

    def get_following(self):
        page = int(math.ceil(self.get_following_num()/50))
        ups = []
        for i in range(1, page+1):
            print('\r获取关注列表：'+str(round((i/page)*100,2))+'%',end=""),
            sys.stdout.flush()
            html = curl.get(url="https://api.bilibili.com/x/relation/followings?vmid="+str(self.mid)+"&pn="+str(i)+"&ps=50&order=asc&jsonp=jsonp")
            lists = js.loads(html)["data"]["list"]
            ups += lists
        return ups

    def get_following_num(self):
        html = curl.get(url="https://api.bilibili.com/x/relation/stat?vmid="+str(self.mid)+"&jsonp=jsonp")
        ups = js.loads(html)["data"]["following"]
        return ups

    def get_up_videos(self, mid, size=20):
        html = curl.get(url="http://space.bilibili.com/ajax/member/getSubmitVideos?mid="+str(mid)+"&pagesize="+str(size)+"&page=1")
        videos = js.loads(html)["data"]["vlist"]
        return videos

    def filter_video(self, data):
        new_data=[]
        for d in data:
            count = conn.count("videos", "aid = '%d'" % d["aid"])
            if count == 0:
                new_data.append(d)
        return new_data

    def progress(self, a, b):
        c = b - a
        s = ''
        for j in range(0, a):
            s += "■"
        for i in range(0, c):
            s += "□"
        # s += "]"
        return s

    def save_ups(self,ups):
        for up in ups:
            count = conn.count("ups", "mid = '%d'" % up["mid"])
            if count == 0:
                conn.insert_db("ups", [{"mid":up["mid"],"face":up["face"],"uname":up["uname"],"mtime":up["mtime"],"sign":up["sign"]}])


if __name__ == "__main__":
    Bilibili = Bilibili(26660079)
    # while True:
    notices = []
    ups = Bilibili.get_following()
    Bilibili.save_ups(ups)
    print("\r")
    print("获取数据：")
    new_video = []
    upnum = len(ups)
    i = 0
    for up in ups:
        i += 1
        print("\r"+Bilibili.progress(i, upnum), end="")
        videos = Bilibili.get_up_videos(mid=up["mid"], size=5)
        new_data = Bilibili.filter_video(videos)
        new_video += new_data
        conn.insert_db("videos", new_data)
        if len(new_data) > 0:
            notices.append({"name": up["uname"],"data":new_data})
    print("\r")
    print("完成！")
    for note in notices:
        print(note["name"] + "更新了视频")
        for video in note["data"]:
            print("     "+video['title'])
    print(" ")
    # time.sleep(60)
