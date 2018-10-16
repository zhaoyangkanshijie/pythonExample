from urllib import parse
from urllib import request
from urllib import error
import json

# url = input("input url\n")
url = "https://www.tp-linkshop.com.cn/Products/SearchNew2"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
values = {
    'page': 1,
    'filter': '',
    'sort': 0,
    'count': 0,
    'type': 0,
    'keyWord': '路由器',
    'c1id': '',
    'c2id': ''
}
try:
    data = parse.urlencode(values).encode('utf-8')
    page = request.Request(url, data, headers)
    jsonData = request.urlopen(page).read().decode('utf-8')
except error.URLError as err:
    print("网络连接错误", err)
else:
    result = json.loads(jsonData)
    print(result['result'])