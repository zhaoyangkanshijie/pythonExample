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

2. 应用实例

```python
from bs4 import BeautifulSoup

# html字符串创建BeautifulSoup对象
soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
# 或者打开本地文件
soup = BeautifulSoup(open('index.html'))
# 格式化输出
print soup.prettify()
#输出第一个 title 标签
print soup.title
#输出第一个 title 标签的标签名称
print soup.title.name
#输出第一个 title 标签的包含内容
print soup.title.string
#输出第一个 title 标签的父标签的标签名称
print soup.title.parent.name
#输出第一个  p 标签
print soup.p
#输出第一个  p 标签的 class 属性内容
print soup.p['class']
#输出第一个  a 标签的  href 属性内容
print soup.a['href']
# soup的属性可以被添加,删除或修改. 再说一次, soup的属性操作方法与字典一样
#修改第一个 a 标签的href属性为 http://www.baidu.com/
soup.a['href'] = 'http://www.baidu.com/'
#删除第一个 a 标签的 class 属性为
del soup.a['class']
##输出第一个  p 标签的所有子节点
print soup.p.contents
#输出第一个  a 标签
print soup.a
#输出所有的  a 标签，以列表形式显示
print soup.find_all('a')
#输出第一个 id 属性等于  link3 的  a 标签
print soup.find(id="link3")
#获取所有文字内容
print(soup.get_text())
#输出第一个  a 标签的所有属性信息
print soup.a.attrs
for link in soup.find_all('a'):
    #获取 link 的  href 属性内容
    print(link.get('href'))
#对soup.p的子节点进行循环输出    
for child in soup.p.children:
    print(child)
#正则匹配，名字中带有b的标签
for tag in soup.find_all(re.compile("b")):
    print(tag.name)
```

3. 详解

* 四大对象种类：print type(soup.a)
1. Tag 通过soup.标签名，获取含整个标签内容，通过soup.标签名.属性/attrs，获取属性数组
2. NavigableString 通过soup.标签名.string，获取含标签内容文字
3. BeautifulSoup 可以获取soup.name
4. Comment 需要处理掉注释
```python
if type(soup.a.string)==bs4.element.Comment:
    print soup.a.string
```

* 遍历文档树

1. 直接子节点

Tag.Tag_child1：直接通过下标名称访问子节点。

Tag.contents：以列表形式返回所有子节点。

Tag.children：生成器，可用于循环访问：for child in Tag.children

2. 所有子孙节点
```python
for child in soup.descendants:
    print child
```

3. 父节点

Tag.parent：父节点

Tag.parents：父到根的所有节点

4. 兄弟节点

Tag.next_sibling

Tag.next_siblings

Tag.previous_sibling

Tag.previous_siblings

5. 前后节点

.next_element

.previous_element

.next_elements

.previous_elements

6. 搜索文档树

find_all( name , attrs , recursive , text , **kwargs )

recursive=False，搜直接子孙节点，否则搜全部子孙节点

```python
import re # 正则搜索
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
# 搜索列表
soup.find_all(["a", "b"])
# True 可以匹配任何值,下面代码查找到所有的tag,但是不会返回字符串节点
for tag in soup.find_all(True):
    print(tag.name)
# 传方法
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

soup.find_all(has_class_but_no_id)
# keyword 参数
soup.find_all(id='link2')
soup.find_all("a", class_="sister")
# text 参数
soup.find_all(text="Elsie")
soup.find_all(text=["Tillie", "Elsie", "Lacie"])
# limit 参数
soup.find_all("a", limit=2)
```

7. CSS选择器搜索
```python
# 所有css表达式，标签名、类名、id 名、组合、属性
soup.select('表达式') 
#遍历
for tag in soup.select('a'):
    print tag.get_text()
```

## pyspider

一个国人编写的强大的网络爬虫系统并带有强大的WebUI。采用Python语言编写，分布式架构，支持多种数据库后端，强大的WebUI支持脚本编辑器，任务监视器，项目管理器以及结果查看器。

参考教程：
* [Python3环境安装PySpider爬虫框架过程](https://www.cnblogs.com/liuliliuli2017/p/6746550.html)
* [手把手教你写网络爬虫（3）：开源爬虫框架对比](http://python.jobbole.com/89095/)
* [Python爬虫-pyspider框架的使用](https://www.jianshu.com/p/1f166f320c66)

1. 安装
```
pip install pyspider
或
sudo apt-get install phantomjs
```
测试
```
pyspider all
```
然后浏览器访问 http://localhost:5000

2. 具体使用

[Python爬虫-pyspider框架的使用](https://www.jianshu.com/p/1f166f320c66)














