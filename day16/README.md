# 今天主要内容
[Django 跨站请求伪造]()

参考:

[Django1.11 Ajax跨站请求](https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax)

## 一、简介

django为用户实现防止跨站请求伪造的功能，通过中间件 django.middleware.csrf.CsrfViewMiddleware 来完成。而对于django中设置防跨站请求伪造功能有分为全局和局部。

django的csrf做了两件事：1.往form表单中写入了csrf_token(普通表单post时用的是这里的token) 2.往cookie中也写入了csrf_token(Ajax post提交时用的是这里的token)

全局：
- 中间件 django.middleware.csrf.CsrfViewMiddleware

局部：
- @csrf_protect，为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件。
- @csrf_exempt，取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
- 注：from django.views.decorators.csrf import csrf_exempt,csrf_protect

## 二、应用
1、普通表单
```
veiw中设置返回值：
　　  return render_to_response('Account/Login.html',data,context_instance=RequestContext(request))　　
     或者
     return render(request, 'xxx.html', data)
   
html中设置Token:
　　{% csrf_token %}
```
2、Ajax

对于传统的form，可以通过表单的方式将token再次发送到服务端，而对于ajax的话，使用如下方式。需要下载导入jquery.cookie.js

urls.py
```
from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^csrf/', views.csrf),
]
```
view.py
```
from django.shortcuts import render,HttpResponse,redirect

def csrf(request):

    return render(request,'csrf.html')
```
csrf.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>csrf跨站请求伪造</title>
</head>
<body>
    <form action="/csrf/" method="post">
        {% csrf_token %}
        <input type="text" name="v"/>
        <input type="submit" value="提交">
    </form>

    <input type="button" value="Ajax提交" onclick="DoAjax();"/>

    <script src="/static/jquery-1.12.4.js"></script>
    <script src="/static/jquery.cookie.js"></script>
    <script>
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        function DoAjax() {
            $.ajax({
                url:'/csrf/',
                type: 'post',
                data:{'k1':'va'},
                sucess:function (data) {
                    console.log(data);
                }
            });
        }
    </script>
</body>
</html>
```
