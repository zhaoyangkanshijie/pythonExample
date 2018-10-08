# pythonExample

爬虫

开发环境：python3+win8.1+pycharm

参考教程：
* [PyCharm 安装教程(Windows)](http://www.runoob.com/w3cnote/pycharm-windows-install.html)
* [python--windows下安装BeautifulSoup](https://www.cnblogs.com/xxoome/p/5870356.html)
* [Python3 爬虫快速入门攻略](https://blog.csdn.net/csdn2497242041/article/details/77170746)

## urllib

urllib用来获取url，抓取远程数据，进行保存。

参考教程：
* [Python3学习笔记（urllib模块的使用）](https://www.cnblogs.com/Lands-ljk/p/5447127.html)
* [Python3中urllib使用介绍](https://blog.csdn.net/duxu24/article/details/77414298)


1. 直接用urllib.request模块的urlopen（）获取页面，page的数据格式为bytes类型，需要decode（）解码，转换成str类型。

```python
from urllib import request
response = request.urlopen(r'http://python.org/')
page = response.read()
page = page.decode('utf-8')
```

urlopen返回对象提供方法：
* read() , readline() ,readlines() , fileno() , close() ：对HTTPResponse类型数据进行操作
* info()：返回HTTPMessage对象，表示远程服务器返回的头信息
* getcode()：返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
* geturl()：返回请求的url

2. 使用request（）来包装请求，再通过urlopen（）获取页面。

```python
url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
req = request.Request(url, headers=headers)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

用来包装头部的数据：
* User-Agent ：这个头部可以携带如下几条信息：浏览器名和版本号、操作系统名和版本号、默认语言
* Referer：可以用来防止盗链，有一些网站图片显示来源http://***.com，就是检查Referer来鉴定的
* Connection：表示连接状态，记录Session的状态。

3. urlopen（）的data参数默认为None，当data参数不为空的时候，urlopen（）提交方式为Post。

```python
from urllib import request, parse
url = r'http://www.lagou.com/jobs/positionAjax.json?'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, headers=headers, data=data)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

经过urlencode（）转换后的data数据为?first=true?pn=1?kd=Python，最后提交的url为

http://www.lagou.com/jobs/positionAjax.json?first=true?pn=1?kd=Python

Post的数据必须是bytes或者iterable of bytes，不能是str，因此需要进行encode（）编码

4. 异常处理

```python
def get_page(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers)
    try:
        page = request.urlopen(req, data=data).read()
        page = page.decode('utf-8')
    except error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))
    return page
```

5. 使用代理

当需要抓取的网站设置了访问限制，这时就需要用到代理来抓取数据。

```python
data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
proxy = request.ProxyHandler({'http': '5.22.195.215:80'})  # 设置proxy
opener = request.build_opener(proxy)  # 挂载opener
request.install_opener(opener)  # 安装opener
data = parse.urlencode(data).encode('utf-8')
page = opener.open(url, data).read()
page = page.decode('utf-8')
return page
```

6. Cookie的使用

爬取的网页涉及登录信息。访问每一个互联网页面，都是通过HTTP协议进行的，而HTTP协议是一个无状态协议，所谓的无状态协议即无法维持会话之间的状态。

```python
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar

url='http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=La2A2'
data={
    'username':'zhanghao',
    'password':'mima',
}
postdata=urllib.parse.urlencode(data).encode('utf8')
header={
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

request=urllib.request.Request(url,postdata,headers=header)
#使用http.cookiejar.CookieJar()创建CookieJar对象
cjar=http.cookiejar.CookieJar()
#使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
cookie=urllib.request.HTTPCookieProcessor(cjar)
opener=urllib.request.build_opener(cookie)
#将opener安装为全局
urllib.request.install_opener(opener)

try:
    reponse=urllib.request.urlopen(request)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)

fhandle=open('./test1.html','wb')
fhandle.write(reponse.read())
fhandle.close()

url2='http://bbs.chinaunix.net/forum-327-1.html'   #打开test2.html文件，会发现此时会保持我们的登录信息，为已登录状态。也就是说，对应的登录状态已经通过Cookie保存。
reponse2=urllib.request.urlopen(url)
fhandle2=open('./test2.html','wb')
fhandle2.write(reponse2.read())
fhandle2.close()
```

## Beautiful Soup

Beautiful Soup是python的一个库，最主要的功能是从网页抓取数据。

参考教程：
* [python beautiful soup库的超详细用法](https://blog.csdn.net/love666666shen/article/details/77512353)
* [python 库安装方法及常用库](https://www.cnblogs.com/yrm1160029237/p/6295988.html)
* [Pycharm中如何安装python库](https://jingyan.baidu.com/article/335530dafdbb3619cb41c3a8.html)
* [python--windows下安装BeautifulSoup](https://www.cnblogs.com/xxoome/p/5870356.html)
* [BeautifulSoup基本用法总结](https://blog.csdn.net/kikaylee/article/details/56841789)

1. 安装

```
pip install beautifulsoup4
pip install lxml
pip install html5lib
```
Beautiful Soup支持Python标准库中的HTML解析器,还支持一些第三方的解析器，如果我们不安装它，则 Python 会使用 Python默认的解析器，lxml 解析器更加强大，速度更快，推荐安装。

|解析器          |使用方法                             |优势      |劣势      |
|---------------|------------------------------------|---------|----------|
|Python标准库    |BeautifulSoup(markup, “html.parser”)|Python的内置标准库<br>执行速度适中<br>文档容错能力强|Python 2.7.3 or 3.2.2)前 的版本中文档容错能力差|
|lxml HTML 解析器|BeautifulSoup(markup, “lxml”)       |速度快<br>文档容错能力强|需要安装C语言库|
|lxml XML 解析器 |BeautifulSoup(markup, [“lxml”, “xml”])<br>BeautifulSoup(markup, “xml”)|速度快<br>唯一支持XML的解析器|需要安装C语言库|
|html5lib       |BeautifulSoup(markup, “html5lib”)|最好的容错性<br>以浏览器的方式解析文档<br>生成HTML5格式的文档|速度慢|
















