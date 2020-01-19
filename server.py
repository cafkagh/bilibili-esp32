# -*- coding: utf-8 -*-
import StringIO

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import Response, Flask

from Download import Download as dld
from Pdo import Pdo as pdo
from img2hex import img2hex as i2h

i2h = i2h()

download = dld()
app = Flask(__name__)

font = ImageFont.truetype('msyh.ttf', 12, encoding="unic")


def SetFixedStrLength(text, width=128):
    print(text)
    strList = []
    newStr = ''
    index = 0
    to_next_line = ''
    for item in text:
        prev_s = newStr
        newStr += item  # after_s
        after_l = font.getsize(newStr)[0]
        to_next_line_l = font.getsize(to_next_line)[0]
        if (after_l + to_next_line_l > width):
            prev_s = to_next_line + prev_s
            to_next_line = item
            strList.append(prev_s)
            newStr = ''
            prev_s = ''
            if font.getsize(text[index:])[0] <= width:
                strList.append(text[index:])
                break
        index += 1
    return ('\n'.join(strList)), len(strList)


@app.route('/')
def return_image():
    conn = pdo(dbtype="sqlite3", database="/home/python/bilibili/bilibili.db")
    info = conn.find(table="videos", order="created desc")
    upinfo = conn.find(table="ups", where="mid = %d" % info["mid"])
    (title, count) = SetFixedStrLength(info["title"])
    im = Image.new('1', (128, 64))
    draw1 = ImageDraw.Draw(im)
    draw1.text((0, 0), upinfo["uname"] + unicode("更新了：", "utf-8"), font=font, fill=1)
    draw1.text((0, 15), title, font=font, fill=1)
    stream = StringIO.StringIO()
    im.save(stream, "JPEG")
    stream.seek(0)
    return Response(stream, mimetype="image/png")


@app.route('/hex')
def return_hex():
    conn = pdo(dbtype="sqlite3", database="/home/python/bilibili/bilibili.db")
    info = conn.find(table="videos", order="created desc")
    upinfo = conn.find(table="ups", where="mid = %d" % info["mid"])
    (title, count) = SetFixedStrLength(info["title"])
    im = Image.new('1', (128, 64))
    draw1 = ImageDraw.Draw(im)
    draw1.text((0, 0), upinfo["uname"] + unicode("更新了：", "utf-8"), font=font, fill=1)
    draw1.text((0, 15), title, font=font, fill=1)
    return (",".join(i2h.tohex(im)))


@app.route('/pic')
def return_pic_image():
    conn = pdo(dbtype="sqlite3", database="/home/python/bilibili/bilibili.db")
    info = conn.find(table="videos", order="created desc")
    imagedata = download.get("http:" + info["pic"]).data
    im = Image.open(StringIO.StringIO(imagedata)).resize((128, 64)).convert('L').filter(ImageFilter.FIND_EDGES)
    stream = StringIO.StringIO()
    im.save(stream, "JPEG")
    stream.seek(0)
    return Response(stream, mimetype="image/jpeg")


@app.route('/pic_hex')
def return_pic_hex():
    conn = pdo(dbtype="sqlite3", database="/home/python/bilibili/bilibili.db")
    info = conn.find(table="videos", order="created desc")
    imagedata = download.get("http:" + info["pic"]).data
    im = Image.open(StringIO.StringIO(imagedata)).resize((128, 64)).convert('1')
    return (",".join(i2h.tohex(im)))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8010, debug=True)
