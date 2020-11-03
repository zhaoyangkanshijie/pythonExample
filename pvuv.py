# -*- coding=utf-8 -*-
from urllib import request

url = "https://www.zybuluo.com/onlineTP/note/1752675"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
brushNum = 100
for i in range(brushNum):
    page = request.Request(url, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')