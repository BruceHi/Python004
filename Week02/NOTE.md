学习笔记

##### 作业说明

1. 作业一：movies 文件夹。用了两种方法，默认运行第一种。

   pipelines.py 是打开数据库，**整体**存储完所有数据，最后关掉。

   2pipelines.py 是每存一条，就打开数据库，存入数据，关掉数据。

2. 作业二：用了两种方法，所以有两个文件 2.1requests.py、2.2selenium.py。

   content.html 是方法一登陆成功下载的页面。

##### 异常

魔法函数：
`__call__`  将函数当成方法调用。
`__str__`  将函数当成字符串打印。
运行 Python 时，打印出错误，是调用了 `trace back` 函数进行追踪。
所有异常从 `baseexception` 继承，而自定义异常要继承 `exception`。

##### `with` 上下文环境的原理
通常在打开文件会用到，例如
```py
with open('test.txt', 'r') as f:
    print(f.read())
```
其实本质上是调用了 `open()` 魔术方法 `enter` 和 `exit`。开始时调用 `enter`，结束时调用 `exit`。

如果 `with` 语句后面明确有 `as` 定义变量，就将调用函数的 `__enter__()` 的返回值赋值给它。这里是将 `__enter__()` 返回的**句柄**赋值给 `f`。
`with` 语句会保证如果  `__enter__()`  方法返回时**未发生**错误，则 `__exit__()` 将总是被调用。
注意：`with` 里面的语句体发生错误了，照样报错。

***
##### `pymysql` 方法分析
使用 `pymysql` 模块操作 `mysql` 完整流程可分为以下几个步骤：

    打开连接 --> 打开游标 -> 操作 (执行 SQL、提交、回滚等)--> 关闭游标 --> 关闭连接。
1. 打开连接。一般只需填写 `host`、`user`、`password`、`database`、`charset` 这几个信息。注意 `utf8mb4` 才是标准的 `mysql` 字符集。当然最好把连接数据库的信息另写入文件。
 ```py
conn = pymysql.connect(host='localhost', user='root', password='123456', database='test', charset='utf8mb4') 
 ```
2. 打开（定义）游标。默认开启了一个事务。
 ```py
 cur = conn.cursor()
 ```
3. 操作。这里也包含了提交操作，回滚操作，这两个操作是由 `conn` 操作。`SQL` 语句是由游标 `cur` 执行的。
当然若只用到查询（DQL），是无需 commit 和 rollback 的。
 ```py
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
 ```
4. 关闭游标（事务）。
 ```py
 cur.close()
 ```
5. 关闭连接。
 ```py
 conn.close()
 ```
###### `execute()` VS. `executemany()`
两者都是**游标**执行 `SQL` 的操作。返回受影响的行数（Number of rows affected）。

`execute(self, query, args=None)`：执行一条语句。
第一个参数是必不可少的，需要 `SQL` 语句。
若是 `SQL` 语句并非完整的，其中数据项使用了 `%s` 代替，这时就需要第二个参数以元组、列表和集合方式传给来了。
```py
sql = 'insert into scores values (%s, %s)'
count = cur.execute(sql, ['18', '2.3'])
```

`executemany(self, query, args)` ：执行多条语句，多用于多行插入或替换。
(str, list) -> int：两个参数必不可少。
```py
sql = 'insert into scores values (%s, %s)'
data = [
    [11, 5],
    [12, 3.6],
    [13, 4.5]
]
count = cur.executemany(sql, data)
```
###### 查询结果显示
若是执行 DQL 命令，可以用以下几种方式取出检索结果（游标 `cursor` 的方法）：
* `fetchone()`：取出游标所指的那条数据。默认顶部。
* `fetchall()`：取出所有数据。
* `fetchmany(size=None)`：取出指定个数数据。默认取出 1 条数据。数据类型：Tuble(Tuble)。一条数据是 `((3, 4.0),)` 这个样子的。

每条数据用**元组**打包返回。若是取出多条数据，也是将所有数据封装成**元组**打包返回。
能得到多少行数据，取决于 `cur.execute(sql)` 的返回值。
由于游标的特性，只能**单向**往下操作，多次取值时要注意：
```
print(cur.fetchall())
print(cur.fetchmany())
print(cur.fetchone())
```
结果，all 取了所有数据之后，游标位于末尾之后，所以再取不到任何数据了。
```
((4, 3.85), (5, 4.0), (6, 3.65), (7, 6.0), (8, 3.0), (9, 4.0), (10, 2.3), (11, 5.0))
()
None
```
***
***
##### HTTP 头部信息
###### User-Agent
可以使用 `fake_useragent.UserAgent` 随机生成 User-Agent，使用 `random` 属性：`ua.random`。
为了方便，定义的时候要去除 ssl 验证。
```
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
print(f'random browser: {ua.random}')
```
###### Referer
表示该页面是由哪一个页面跳转过来的。
一般都是连接：
比如：`'Referer': 'https://accounts.douban.com/passport/login?source=movie'`

###### Cookies
 Cookies 存储的是用户的本地信息。我们可以通过打开浏览器，进行复制过来。
但是大多时候，只有在用户**登陆**成功的网站，Cookies 才有作用。另外 Cookies 有时限，需要动态获取。

我们可以通过 `requests` 的会话机制得到 Cookies。
1. 首先定义会话：`s = requests.Session()`。
2. 使用未带 Cookies 信息的 `header` 对目标网站发送 post 或 get 请求，只要请求成功，就会得到 Cookies：
`s.cookies`。打印出来，类似于这种： `<RequestsCookieJar[<Cookie sessioncookie=12345678 for httpbin.org/>]>`。
3. 对目标网站发送请求时，就可以使用该 Cookies 了。

一般用于需要登陆，获取特定信息的网站。
或是你预感到了若对该网页进行大量请求，会有反爬。也可以在第一次访问就获取到 Cooies，然后每次请求都更新 Cooies。不过有更好的方法进行爬虫，我猜这种方法用得不多。

***
##### `webdriver` 自动化测试
主要可以分为以下步骤：
1. 导入该模块：`from selenium import webdriver`。
2. 调起浏览器：`driver = webdriver.Chrome()`，这里是打开谷歌浏览器。
3. 打开目标网页：`driver.get('https://www.douban.com')`，注意没有 post。
4. 定位到元素：`button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')`。这里定位到一个按钮元素。
5. 对元素进行操作：点击、填充表单：`btm1.click()`、`pass.send_keys('test123test456')` 等其他操作。
6. 关闭浏览器：`driver.close()`。可选。

###### 元素定位
元素定位是 `webdriver` 最为关键的步骤。
获取一个 `WebElement` 元素：可以使用  `find_element_by_id`、`find_element_by_tag_name`、`find_element_by_xpath` 等多种方法定位。

若是找不到该元素，返回 `NoSuchElementException`。
若是一下子找到多个元素，返回第一个元素。（没有进行充分测试。）

建议使用**准确**定位，id、xpath 等可以定义到唯一一个的方式。
若该标签有 id 属性，第一个想法就是通过 id 定位。因为 id 在整个页面是唯一的。

比如下面两种方法是相同的，但通过 id 更为方便，尽管第二种方法是通过 xpath 语法的 id 定位的：
```py
driver.find_element_by_id('username')
driver.find_element_by_xpath('//*[@id="username"]')  # 注意 * 代表匹配任何元素节点。
```

寻找多个元素，返回是一个列表，即使是没找到，也只是返回空列表。
上面所有的方法，都有对应的找多个元素方法，只是将前者的 `element` 变为了 `elements`：`find_elements_by_xpath`、`find_elements_by_link_text` 等等。
写的时候千万别写错了。

***
***
##### 随机代理
步骤：
1. 进入 `seting.py`。
在 53 行左右，去掉 `DOWNLOADER_MIDDLEWARES` 的注释。并添加自定义中间件的位置及优先级：
`'randproxy.middlewares.RandomHttpProxyMiddleware': 400`。`randproxy.middlewares` 代表模块位置，`RandomHttpProxyMiddleware` 是自定义类。这里**数字**越小，优先级越高。
若用不到某些中间键，可能将数字改为 `None`。
并在其后添加代理列表，`HTTP_PROXY_LIST`，最好使用大写。
2. 在 `middlewares.py` 编写自己的类。
##### 自定义中间件流程分析
1、首先是定义装饰器类方法，返回**类**对象，该对象正好带两个参数，一个参数是编码，另一个是从 `setting.py` 获得的代理列表。
```py
@classmethod
def from_crawler(cls, crawler):
    if not crawler.settings.get('HTTP_PROXY_LIST'):
        raise NotConfigured
    http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
    auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
    return cls(auth_encoding, http_proxy_list)
```
2、该类对象携带的参数，正好可以用于初始化对象。最重要的就是设置属性 `proxies`。该属性使用字典来存储协议和代理地址。
```
def __init__(self, auth_encoding='utf-8', proxy_list=None):
    super().__init__(auth_encoding)
    self.proxies = defaultdict(list)
    for proxy in proxy_list:
        parse = urlparse(proxy)
        self.proxies[parse.scheme].append(proxy)
```
3、设置代理，从所给的**协议**中随机选取一个（使用字典的原因），然后通过 `Request.meta['proxy']` 读取 `http_proxy` 环境变量加载代理。
```py
def _set_proxy(self, request, scheme):
    proxy = random.choice(self.proxies[scheme])
    request.meta['proxy'] = proxy
```

***

scrapy 写了刚学的一些。

xpath 一点也没写，上次留得坑，这次还没填。哎……




