from urllib import request
from urllib import error
from bs4 import BeautifulSoup  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库
from queue import Queue
import re
import time

'''
功能描述：爬取网站节点下所有链接
思路：
    1.爬取首页所有链接
        过滤无效链接，如（javascript:void(0)）
        过滤外部链接（出现www.***.com的外链）
        所以，有效链接为：
            /...
            url + "/..."
        把所有链接存入队列
    2.在队列中广度优先爬取次级页面链接
        过滤重复链接
问题：
    1.为什么使用广度优先搜索？
        这样爬出来的网页结构根平坦，不会大多子链接都以第一个链接为祖先元素
    2.为什么不类似于书本目录，层级输出搜索结果？
        层级输出用的是深度优先搜索的方法实现，所以需要用多层数组储存数据，并递归输出，但遇到的问题有：
            需要知道链接在第几层级
            需要知道链接父子节点关系，以处理兄弟和同辈关系
        这样会导致数据结构复杂，且占用内存大，或查找插入文本操作麻烦，故没有实现。
'''

globalQueue = Queue()  # 用于广度优先搜索
globalSet = set()  # 用于全局去重
badURL = []  # 用于储存打不开的链接
firstTime = time.time()  # 运行初始时间

# url = input("input url\n")
# url = url.strip()
# if url[-1] == "/":
#     url = url[0:len(url)-1]
# print(url)

url = "https://www.tp-link.com.cn"
globalQueue.put(url)
pattern = re.compile("www." + '(.*?)' + ".com")
domain = pattern.findall(url)
print(domain)

# 限制待打开页面数量queueLimitLength，到达此数量时，终止程序
# 限制结果数量resultLimitLength，到达此数量时，终止程序
# 限制程序运行秒数runTimeSecondLimit，到达此数量时，终止程序
def getLinks(queueLimitLength = 99999,resultLimitLength = 99999, runTimeSecondLimit = 9999):
    # 构造头文件，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    currentQueueLength = 1  # 当前队列长度
    while not globalQueue.empty():
        # print(firstTime, time.time())
        if time.time() - firstTime > runTimeSecondLimit:
            break
        if currentQueueLength > queueLimitLength:
            break
        if len(globalSet) > resultLimitLength:
            break

        tempURL = globalQueue.get()
        currentQueueLength = currentQueueLength - 1
        print(tempURL)

        try:
            page = request.Request(tempURL, headers=headers)
            page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
        except error.URLError as err:
            print("网络连接错误", err)
            badURL.append(tempURL)   # 打不开的链接
            continue
        else:
            # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
            soup = BeautifulSoup(page_info, 'html.parser')

            # 以格式化的形式打印html
            # print(soup.prettify())

            pageLinks = soup.find_all('a')  # 查找所有a标签

            '''
            链接含有url?
                是：内链，去重加入
                否：检查含有"/"且没"http"？
                    是：添加url后去重加入
                    否：丢弃
            '''
            localSet = set()  # 用于局部去重
            for pageLink in pageLinks:
                try:
                    tempLink = pageLink.get("href")
                    if tempLink is None:
                        continue
                    if tempLink.find(url) != -1:
                        if tempLink not in globalSet:
                            # print('1:', tempLink, globalSet, tempLink in globalSet)
                            localSet.add(tempLink)
                            globalSet.add(tempLink)
                    else:
                        if tempLink.find("/") != -1 and tempLink.find("http") == -1:
                            if url + tempLink not in globalSet:
                                # print('2:', tempLink, globalSet, tempLink in globalSet)
                                localSet.add(url + tempLink)
                                globalSet.add(url + tempLink)
                except ValueError as err:
                    print("链接出错：", err)
                    continue

            print(len(localSet), localSet)
            print(len(globalSet), globalSet)

            for href in localSet:
                globalQueue.put(href)
                currentQueueLength = currentQueueLength + 1

            print("当前队列长度:", currentQueueLength)

            del localSet

            # time.sleep(5)


getLinks(1000, 2000, 10)

# open()是读写文件的函数,with语句会自动close()已打开文件
with open(r"D:\项目\pythonExample\webLinks.txt", "w", encoding='utf-8') as file:
    file.write("链接个数：" + str(len(globalSet)) + '\n\n')
    for item in globalSet:
        file.write(item + '\n\n')

with open(r"D:\项目\pythonExample\webBadLinks.txt", "w", encoding='utf-8') as badFile:
    badFile.write("无法访问链接个数：" + str(len(badURL)) + '\n\n')
    for item in badURL:
        badFile.write(item + '\n\n')

