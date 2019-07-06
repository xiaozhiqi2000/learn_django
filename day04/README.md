# 今天主要内容
1. [django Urls路由系统]()

参考：

[Django1.11 官网urls](https://docs.djangoproject.com/en/1.11/topics/http/urls/)


### 1.路由系统格式
```
urlpatterns = [
    url(正则表达式, views视图函数, 参数, 别名name=""),
    url(r'^index/(\d*)', views.index, {'id':333}, name="test")
]

# 别名name="test",和static和upload中的别名是一样的作用,后端路由怎么变,前端引用的都是别名
# 比如form中 <form action="{% url "test" %}" method="post"></form> action引用test这个别名这样就提交给 views.index这个方法
```

### 2.url通过正则表达式传参
有分组,后端view即需要参数接收,前端传过来的是字符串
```
url(r'^index/(\d*)', views.index),
url(r'^list/(\d*)/(\d*)/$', views.list),   
url(r'^manage/(?P<name>\w*)/(?P<id>\d*)', views.manage),
url(r'^login/(?P<name>\w*)', views.login,{'id':333}),
url(r'^login/(?P<id>[0-9]{4})', views.login,{'id':333}),  #id:333会覆盖掉前面匹配到的值
```
views如何接收参数？
```
def index(request,id):  # id形参的名字是随便定义的
    
    return render_to_response('index.html')

    
def list(request,id1,id2): # id1,id2形参的名字是随便定义的
    
    return render_to_response('list.html')


def manage(request,name,id):  # name,id形参的名字是和(?P<name>\w*)/(?P<id>\d*)是一样的
    
    return render_to_response('index.html')


def login(request,name,id):  # name,id形参的名字是和(?P<name>\w*)，{'id':333}是一样的
    
    return render_to_response('login.html')
```

### 3.url路由分发
例如我的mysite项目中创建了2个app,blog和jumpserver

mysite,blog,jumpserver中各有urls.py路由文件
```
(py36) [root@localhost ~]# tree mysite
mysite
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── jumpserver
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static
└── upload

```
mysite中的urls.py是mysite项目的总路由,进行路由分发
```
from django.conf.urls import include
 
urlpatterns = patterns[
    url(r'^blog/', include('blog.urls')),
    url(r'^jumpserver/', include('jumpserver.urls')),
]
```
blog中的urls.py
```
from django.conf.urls import url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'news/', views.news),
    url(r'book/', views.book),
]

```
jumpserver中的urls.py
```
from django.conf.urls import url
from django.contrib import admin
from jumpserver import views

urlpatterns = [
    url(r'users/', views.users),
    url(r'hosts/', views.hosts),
]
```
django中的路由系统和其他语言的框架有所不同，在django中每一个请求的url都要有一条路由映射，这样才能将请求交给对一个的view中的函数去处理。其他大部分的Web框架则是对一类的url请求做一条路由映射，从而是路由系统变得简洁
