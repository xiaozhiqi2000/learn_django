# 今天主要内容

参考:

[Django1.11 中间件](https://docs.djangoproject.com/en/1.11/ref/middleware/)

[Django1.11 自定义中间件](https://docs.djangoproject.com/en/1.11/topics/http/middleware/)


## 一、middleware

先看看中间件是在HTTP中哪个过程

![avatar](/day16/imgs/161.png)

django 中的中间件（middleware），在django中，中间件其实就是一个类，在请求到来和结束后，django会根据自己的规则在合适的时机执行中间件中相应的方法。

在django项目的settings模块中，有一个 MIDDLEWARE_CLASSES 变量，其中每一个元素就是一个中间件，每一个中间件是一个类，类中不一定要写5个方法

```
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
中间件中可以定义五个方法，分别是：（主要的是process_request和process_response）
- process_request(self,request)
- process_view(self, request, callback, callback_args, callback_kwargs)
- process_template_response(self,request,response)
- process_exception(self, request, exception)
- process_response(self, request, response)   最后必须return response

以上方法的返回值可以是None或一个HttpResponse对象，如果是None，则继续按照django定义的规则向后继续执行，如果是HttpResponse对象，则直接将该对象返回给用户。

当用户发起请求的时候会依次经过所有的的中间件，这个时候的请求时process_request,最后到达views的函数中，views函数处理后，在依次穿过中间件，这个时候是process_response,最后返回给请求者。

![avatar](/day16/imgs/16.png)

请求先通过中间件执行所有的process_request方法，然后再执行process_view方法，然后执行views中的方法，

如果views中的方法包含render_to_response()方法则会执行process_template_response方法，如果views中的

方法执行错误了，则会执行process_exception方法，最后执行process_response方法。

## 二、自定义中间件
1.创建中间件类
```
from django.utils.deprecation import MiddlewareMixin

class defindemiddleware(MiddlewareMixin):
       
    def process_request(self,request):
        print(123)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print(456)

    def process_exception(self, request, exception):
        print(error)

    def process_response(self, request, response):
        print(end)
        return response
```
2.注册中间件
```
MIDDLEWARE_CLASSES = (
    'my.middleware.defindedmiddleware',     # 目录结构my/middleware/类名
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
```

## 三、一个简单的例子
高流量的站点通常需要将Django部署在负载平衡proxy之后。 这种方式将带来一些复杂性，其一就是每个request中的远程IP地址(request.META["REMOTE_IP"])将指向该负载平衡proxy，而不是发起这个request的实际IP。 负载平衡proxy处理这个问题的方法在特殊的 X-Forwarded-For 中设置实际发起请求的IP。

因此，需要一个小小的中间件来确保运行在proxy之后的站点也能够在 request.META["REMOTE_ADDR"] 中得到正确的IP地址
```
class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip
```
