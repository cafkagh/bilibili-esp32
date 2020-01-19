# bilibili-esp32
**esp32显示关注的up更新**
#

**bilibili.py--获取更新**
- Bilibili = Bilibili(你的mid)
- 建议使用 crontab 定时运行

**service.py--输出最后一条更新信息**
*使用flask提供webapi*
- app.run(host="0.0.0.0", port=你想设置的端口, debug=False)
#

文字图像：ip:port/ 
*例 http://47.52.231.64:8010/*

文字HEX：ip:port/hex
*例 http://47.52.231.64:8010/hex*


封面图像：ip:port/pic
*例 http://47.52.231.64:8010/pic*

封面HEX：ip:port/pic_hex
*例 http://47.52.231.64:8010/pic_hex*
