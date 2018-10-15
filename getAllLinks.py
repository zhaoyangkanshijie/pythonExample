from urllib import request
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
    3.可考虑根据"/"重新聚类链接
记录：
    1.解决循环链接问题，局部链接去重后，还要全局链接去重
'''

globalQueue = Queue()  # 用于广度优先搜索
globalSet = set()  # 用于全局去重
badURL = []  # 用于储存打不开的链接
firstTime = time.time()  # 运行初始时间

url = input("input url\n")
url = url.strip()
print(url)

# url = "https://www.tp-link.com.cn"
globalQueue.put(url)
pattern = re.compile("www." + '(.*?)' + ".com")
domain = pattern.findall(url)
print(domain)

def getLinks(queueLimitLength = 99999,runTimeSecondLimit = 9999):
    # 构造头文件，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    currentQueueLength = 1  # 当前队列长度
    while not globalQueue.empty():
        if time.time() - firstTime > runTimeSecondLimit:
            break
        if currentQueueLength > queueLimitLength:
            break

        tempURL = globalQueue.get()
        currentQueueLength = currentQueueLength - 1
        print(tempURL)

        try:
            page = request.Request(tempURL, headers=headers)
            page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
        except ValueError as err:
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
                            localSet.add(tempLink)
                        globalSet.add(tempLink)
                    else:
                        if tempLink.find("/") != -1 and tempLink.find("http") == -1:
                            if tempLink not in globalSet:
                                localSet.add(tempLink)
                            globalSet.add(url + tempLink)
                except ValueError as err:
                    print("链接出错：", err)
                    continue

            print(len(localSet), localSet)

            for href in localSet:
                globalQueue.put(href)
                currentQueueLength = currentQueueLength + 1

            print("当前队列长度:", currentQueueLength)

            del localSet

            # time.sleep(5)


getLinks()

# open()是读写文件的函数,with语句会自动close()已打开文件
with open(r"D:\项目\pythonExample\webLinks.txt", "w", encoding='utf-8') as file:
    for item in globalSet:
        file.write(item + '\n\n')

with open(r"D:\项目\pythonExample\webBadLinks.txt", "w", encoding='utf-8') as file:
    for item in badURL:
        file.write(item + '\n\n')