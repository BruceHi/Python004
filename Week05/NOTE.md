### 作业说明
作业1：movie

作业2、3：myDjango
### Django 简单流程
#### 1. 创建项目
切换至要放代码的目录，运行：
```
> django-admin startproject mysite
```
则会创建以下文件：

    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            wsgi.py

#### 2. 创建应用
在 Django 中，每一个应用都是一个 Python 包。
切换到 manage.py 所在目录，执行：
```cmd
> py manage.py startapp polls
```
#### 3. 初始设置
到 setting.py 里进行一些常用的设置：
1.增加应用。43 行左右，在列表尾部增加应用名：
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'Douban',
]
```
2.修改数据库配置。
84 行左右，修改。
使用 pymysql 作为 MySQL 的一个引擎。其中 mysql 本地默认 ip 为：127.0.0.1，也可使用 localhost。
python 3 中还要 `pip install mysqlclient`
示例：
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db1',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
3.修改时区。
更改两个位置：
```py
```
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False
```

#### 4. URL 调度
包括两个方面：
1.在根 URLconf 文件（urls.py）使用 `include()` 引入所需模块（应用）。
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]
```
2.重建应用路由配置。
index 是我们所创建的应用。`index.urls` 是指要引入这个。所以，还要再在 index 路径下新建 urls.py 文件。
```
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.show),  # 同样可以匹配以 index？为开头的所有字段。
]
```
和上面一样，里面只有 `urlpatterns` 这一个列表。`path`，`re_path`，`include` 都是比较常用的方法。

#### 5. 模型
首先，需要进行数据库配置，这一步很早就做了。
models.py **定义**了与数据库相关的模型，可以通过**对象关系映射器（ORM）**进行后续的操作
 
model.py 可以**自己创建**，必须要设置**主键**（`primary_key=True`）。默认不写主键，会自动创建一个 `id` 主键。
另外，`primary_key` 和 `null` 不能同时设置为 `True`。否则会报错。
将定义好的模型写入数据库中，需要执行两步：
```
> python manage.py makemigrations
> python manage.py migrate
```

还可以使用逆向工程：由已经存在的 SQL 数据表转换为 models。
```
> python manage.py inspectdb  # 在终端显示
> python manage.py inspectdb > models.py  # 输出文件
```
示例：反向生成的 models.py
```py
from django.db import models


class Shorts(models.Model):
    # 反向生成的也不显示 id。
    short = models.CharField(max_length=400, blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)
    record_time = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shorts'
```

#### 6. 视图
视图是模型的映射。即要展示什么东西，可以在这里定义。可以使用 orm 检索数据。
注意到第四步里，`views.show` 这里就紧接着视图（views.py）的自定义函数 `show` 方法。

例如，下面定义了一个 show 方法。
```
def show(request):
    shorts = Shorts.objects.filter(star__gt=3)

    if 'q' in request.GET:
        # 从已选到的过滤。获取 url 传过来的参数：request.GET['q']，request.GET 是字典。
        shorts = shorts.filter(short__contains=request.GET['q'])

    return render(request, 'index.html', locals())
```
#### 7. 模板
借助模板，我们可以更**漂亮**地展示页面。
我们需要自己建立 templates 文件夹。

上一步所展示的例子，就将结果绑定到了 templates 下面的 index.html 文件（自己创建的，我们最终看到的）。
通过 Django 内建的模板标签和过滤器，可以展示从 views.py 获得的变量。

示例：
```html
{% for short in shorts %}
<tr>
    <th>{{ short.id }}</th>
    <td>{{ short.short }}</td>
    <td>{{ short.star }}</td>
   <td class="text-nowrap">{{ short.record_time|date:"Y-m-d" }}</td> <!-- 格式化时间 -->
</tr>
{% endfor %}
```







