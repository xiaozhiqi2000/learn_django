# 今天主要内容
[django Cookie、Session]()


## 一、为什么需要Cookie or Session
在一个会话的多个请求中共享数据，这就是会话跟踪技术。例如在一个会话中的请求如下：  请求银行主页； 
- 请求登录（请求参数是用户名和密码）；
- 请求转账（请求参数与转账相关的数据）； 
- 请求信誉卡还款（请求参数与还款相关的数据）。  

在这上会话中当前用户信息必须在这个会话中共享的，因为登录的是张三，那么在转账和还款时一定是相对张三的转账和还款！这就说明我们必须在一个会话过程中有共享数据的能力。

HTTP是无状态,每一个请求,对服务器都是新的请求,服务器不知道客户端是谁,所以浏览器带着cookie或者session,服务器就知道你是否来过,你是谁

web开发中使用session来完成会话跟踪,sessionid存在cookie中的键值对,所以session依赖Cookie技术,django中的cookie默认是保存2周时间，用cookie可以做登录验证、多少周保持登录

cookie是存在客户端,session是存在服务器

## 二、Cookie
### 1.Cookie传递过程与本质
Cookie是key-value结构,类似于一个python的字典 ,随着服务器端的响应发送给客户端浏览器,然后客户端浏览器会把Cookie保存起来,当下一次访问服务器时把cookie再发给服务器.

- cookie是由服务器创建,然后通过响应发送给客户端的一个键值对
- Cookie是保存在客户端浏览器中的,并会标记出Cookie的来源(哪个服务器)
- Cookie的本质是在请求头中设置了header,set-cookie: 'key'='value'

当客户端向服务器发出请求时会把所有这个服务器的Cookie在请求中发送给服务器,这样服务器就可以识别客户端
### 2.Cookie 规范
- Cookie大小上限为4KB； 
- 一个服务器最多在客户端浏览器上保存20个Cookie； 
- 一个浏览器最多保存300个Cookie；  
### 3.Cookie 实例配置
url.py配置
```
urlpatterns = [
    url(r'^login/', views.login),
    url(r'^index/', views.index),
]
```
views.py配置
```
import datetime
def index(request):
    print(request.COOKIES)  # 打印cookie
    is_login = request.COOKIES.get("is_login")
    if is_login != '1':
        return redirect("/login/")
    username =request.COOKIES.get("username")#获取cookies的username值
    time=request.COOKIES.get("login_time")
    return render(request, "index.html",{"username":username,"login_time":time})

def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == "zaizai" and pwd == "123":
            obj = redirect("/index/")        # 302重定向登陆页面
            obj.set_cookie("is_login", 1, 5)  # cookie设置登陆状态,设置为5秒钟，cookie失效,默认是2周
            obj.set_cookie("username", user)
            now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            obj.set_cookie("login_time",now)

            return obj
    return render(request, "login.html")
```
index.html
login.html

## 三、Session

参考：

[Django1.11 官网sessions](https://docs.djangoproject.com/en/1.11/topics/http/sessions/)

[Django1.11 官网sessions](https://docs.djangoproject.com/en/1.11/ref/settings/#settings-sessions)


session要比cookie用的更多，因为cookie不安全,session是基于cookie开发的。思路和cookie是不一样的,它们之间最大的不同在于，session存在服务器。而cookie存储在浏览器中！

Django中默认支持Session，其内部提供了5种类型的Session供开发者使用：
- 数据库（Django默认支持Session，并且默认是将Session数据存储在数据库中，即：django_session 表中,django.contrib.sessions.models.Session这个model实现）
- 缓存
- 文件
- 缓存+数据库
- 加密cookie

### 1.sessions存储在settings中的配置

参考：

[Django1.11 官网 session_engine](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SESSION_ENGINE)
```
# 1.sessions数据库存储在settings中的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.db'            # 引擎（默认）,在django_session这张表

# 2.sessions内存存储在settings中的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'         # 引擎
SESSION_CACHE_ALIAS = 'default'                                   # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
 
# 3.sessions文件存储在settings中的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.file'          # 引擎
SESSION_FILE_PATH = None                                          # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir() 
                                                                  # 如：/var/folders/d3/j9tj0gz93dg06bmwxmhh6_xm0000gn/T

# 4.sessions内存和数据库存储在settings中的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'     # 引擎

# 5.sessions加密cookies存储在settings中的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'# 引擎

SESSION_COOKIE_NAME = "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid=随机字符串（默认）
SESSION_COOKIE_PATH = "/"                               # Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）
```

### 2.sessions的方法
```
def index(request):
    # 获取、设置、删除Session中数据
    request.session['k1']
    request.session.get('k1',None)
    request.session['k1'] = 123
    request.session.setdefault('k1',123) # 存在则不设置
    request.session.flush()    # 清理session删除当前的会话数据并删除会话的Cookie这用于确保前面的会话数据不可以再次被用户的浏览器访问
    del request.session['k1']  # 清理某个session

    # 所有 键、值、键值对
    request.session.keys()
    request.session.values()
    request.session.items()
    request.session.iterkeys()
    request.session.itervalues()
    request.session.iteritems()


    # 用户session的随机字符串
    request.session.session_key

    # 将所有Session失效日期小于当前日期的数据删除
    request.session.clear_expired()

    # 检查 用户session的随机字符串 在数据库中是否
    request.session.exists("session_key")

    # 删除当前用户的所有Session数据
    request.session.delete("session_key")
```
### 3.实例配置
url.py配置
```
urlpatterns = [
    url(r'^session_login/', views.session_login),
    url(r'^session_index/', views.session_index),
    url(r'^session_logout/', views.session_logout),
]
```
views.py配置
```
from django.shortcuts import render, redirect

def session_login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('pwd')
        if password == '123' and user == 'xiaoxiao':
            request.session['username'] = user
            return redirect('/session_index/')
    return render(request,'session_login.html')

def auth(func):
    def inner(request,*args,**kwargs):

        user = request.session.get('username',None)
        if not user:
            return redirect('/session_login/')
        return func(request,*args,**kwargs)

    return inner

@auth
def session_index(request):
    user = request.session.get('username',None)
    return render(request,'session_index.html',{'username':user})

@auth
def session_logout(request):
    request.session.flush()
    return redirect('/session_login/')
```
本地文件session_login.html  session_index.html


### 4.分析django 怎么将session写入cookie中
设置session过程request.session['username'] = user 在session中设置属性的时候,django做了两件事：

1.往客户端的cookie中写入了sessionid和随机字符串
![avatar](/day12/imgs/121.png)

2.默认在数据库django_session中插入session_key,session_data,expire_date
![avatar](/day12/imgs/12.png)

