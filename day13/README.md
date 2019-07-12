# 今天主要内容
[django Cache缓存]()

参考：

[Django1.11 官网Cache](https://docs.djangoproject.com/en/1.11/topics/cache/)

## 一、Django Cache 概述
### 1.为什么需要缓存

动态网站的基本权衡是，它们是动态的。 每次用户请求页面时，Web服务器都会进行各种计算 - 从数据库查询到模板呈现再到业务逻辑 - 以创建站点访问者看到的页面。 从处理开销的角度来看，这比标准的文件读取文件系统服务器安排要昂贵得多。最简单解决方式是使用：缓存，缓存将一个某个views的返回值保存至内存或者Memcache或者Redis服务器中，5分钟内再有人来访问时，则不再去执行view中的操作，而是直接从内存或者Memcache或者Redis中之前缓存的内容拿到，并返回。

### 2.Django缓存分类
Django缓存类型:
- Dummy caching (for development)  #调试模式，实际django不做任何操作
- Memcached   #Memcache缓存服务器最有效、最快
- Database caching     #数据库缓存
- Filesystem caching   #文件系统缓存
- Local-memory caching  #本地服务器内存
- Using a custom cache backend(Redis) #Redis缓存服务器需要第三方支持

缓存粒度分类:
- per-site cache   整个网站的缓存
- per-view cache   调用缓存装饰器进行对views中的方法缓存
- template fragment caching  模板缓存
- low-level cache API        低级缓存,对于经常变化的

## 二、各种缓存在Settings.py的配置
这里举例Dummy caching和memcache和reids,其他缓存参考官网,因为其他效率不高
### 1.Dummy caching
```
# 此为开始调试用，实际内部不做任何操作
# 配置：
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',     # 引擎
            'TIMEOUT': 300,                                               # 缓存超时时间（默认300，None表示永不过期，0表示立即过期）
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                       # 最大缓存个数（默认300）
                'CULL_FREQUENCY': 3,                                      # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
            },
            'KEY_PREFIX': '',                                             # 缓存key的前缀（默认空）
            'VERSION': 1,                                                 # 缓存key的版本（默认1）
            'KEY_FUNCTION' 函数名                                          # 生成key的函数（默认函数会生成为：【前缀:版本:key】）
        }
    }


# 自定义key
def default_key_func(key, key_prefix, version):
    """
    Default function to generate keys.

    Constructs the key used by all other methods. By default it prepends
    the `key_prefix'. KEY_FUNCTION can be used to specify an alternate
    function with custom key making behavior.
    """
    return '%s:%s:%s' % (key_prefix, version, key)

def get_key_func(key_func):
    """
    Function to decide which key function to use.

    Defaults to ``default_key_func``.
    """
    if key_func is not None:
        if callable(key_func):
            return key_func
        else:
            return import_string(key_func)
    return default_key_func
```
### 2.Memcache 缓存服务器
```
# 此缓存使用python-memcached模块连接memcache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': '127.0.0.1:11211', #单台memcache服务器
        # 多台memcache服务器设置
        'LOCATION': [ 
            '172.19.26.240:11211',
            '172.19.26.242:11211',
        ]     }
}

# memcache监听socket
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}   
```
### 3.1 第一种 Django Redis 缓存服务器
最新django-redis 4.10支持django 1.11+ 依赖 redis-server 2.8.x+, redis-py >= 2.10.0

参考:

[django-redis github](https://github.com/niwinz/django-redis)

[django-redis文档](http://niwinz.github.io/django-redis/latest/)

#### 安装 django-redis
```
pip install django-redis
```
#### settings.py配置redis缓存
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/1", # 单台redis服务器
        # 多台redis服务器,第一个是master节点,第二个slave节点,官方说主从没有在生产环境大量测试
        "LOCATION": [
            "redis://127.0.0.1:6379/1",
            "redis://127.0.0.1:6378/1",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "mysecret"  # redis密码
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,   # in seconds
            "IGNORE_EXCEPTIONS": True,  # 忽略异常
        }
    }
}
```
#### session配置redis缓存
```
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```
#### 

### 3.2 第二种 Django Redis 缓存服务器
最新django-redis-cache 2.0.0支持django 1.11+ 依赖 redis-server 2.8.x+, redis-py >= 2.10.0

参考:

[django-redis第三方支持github](https://github.com/sebleier/django-redis-cache)

[django-redis第三方支持文档](https://django-redis-cache.readthedocs.io/en/latest/)

#### 安装 django-redis
```
pip install django-redis-cache
```
#### settings.py配置redis缓存
```
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        # 'LOCATION': '127.0.0.1:6379', ## 单台redis服务器
        # 多台redis服务器,第一个是master节点,第二个slave节点,官方说主从没有在生产环境大量测试
        'LOCATION': [
            '127.0.0.1:6379',  # Primary
            '127.0.0.1:6380',  # Secondary
            '127.0.0.1:6381',  # Secondary
        ],
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': 'yadayada',
            'MASTER_CACHE': '127.0.0.1:6379',
            'PARSER_CLASS': 'redis.connection.HiredisParser',  # 需要安装pip install hiredis,Default Parser: redis.connection.PythonParser
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'PICKLE_VERSION': -1,
            'SOCKET_TIMEOUT': 5,
            'SOCKET_CONNECT_TIMEOUT': 5,
        },
        'TIMEOUT': 480,
    },
}
```

## 三、Django如何使用缓存
https://docs.djangoproject.com/en/2.2/topics/cache/#the-per-site-cache

https://docs.djangoproject.com/en/2.2/topics/cache/#the-per-view-cache

https://docs.djangoproject.com/en/2.2/topics/cache/#template-fragment-caching

### 1.中间件缓存整个站点
使用中间件，经过一系列的认证等操作，如果内容在缓存中存在，则使用FetchFromCacheMiddleware获取内容并返回给用户，当返回给用户之前，判断缓存中是否已经存在，如果不存在则UpdateCacheMiddleware会将缓存保存至缓存，从而实现全站缓存
```
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

CACHE_MIDDLEWARE_ALIAS = "default" #用于存储的缓存别名。
CACHE_MIDDLEWARE_SECONDS = 86400      #每个页面应缓存的秒数。
CACHE_MIDDLEWARE_KEY_PREFIX = ""  #如果使用相同的Django安装在多个站点之间共享缓存，请将其设置为站点名称或此Django实例唯一的其他字符串，以防止发生密钥冲突。 如果你不在乎，请使用空字符串。
```
### 2.url或者view方式进行缓存
```
# 第一种在url配置缓存
from django.views.decorators.cache import cache_page
from app01 import views

urlpatterns = [
    url(r'^cachepage/',cache_page(60 * 15)(views.cacheview),name='cachepage'),
]

# 第二种在view配置缓存
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def cacheview(request):
    return render(request,'index.html')
```
### 3.tempalte局部缓存
```
# 第一种引入TemplateTag

{% load cache %}

# 第二种使用缓存

{% cache 5000 缓存key %}  # 5000秒
    缓存内容
{% endcache %}
```
