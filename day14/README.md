# 今天主要内容
[Ajax]()

## 一、Ajax 预备知识(json进阶)
[Json进阶知识](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/jsonAdvance.md")

## 二、Ajax
### 1.Ajax 概述
对于WEB应用程序：用户浏览器发送请求，服务器接收并处理请求，然后返回结果，往往返回就是字符串（HTML），浏览器将字符串（HTML）渲染并显示浏览器上。

通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。传统的网页（不使用 AJAX）如果需要更新内容，必须重载整个网页页面。

AJAX，Asynchronous JavaScript and XML (异步的JavaScript和XML)，一种创建交互式网页应用的网页开发技术方案.
- 异步的JavaScript,使用JavaScript以及相关浏览器提供类库的功能向服务端发送请求，当服务端处理完请求之后，自动执行某个JavaScript的回调函数.
- XML,XML是一种标记语言，是Ajax在和后台交互时传输数据的格式之一，此外还有jsonp格式

何为同步异步
- 同步交互：客户端发出一个请求后，需要等待服务器响应结束后，才能发出第二个请求；
- 异步交互：客户端发出一个请求后，无需等待服务器响应结束，就可以发出第二个请求。

AJAX除了异步的特点外,还有一个特点是:**浏览器页面局部刷新**

利用AJAX可以做：
- 注册时，输入用户名自动检测用户是否已经存在。
- 登陆时，提示用户名密码错误
- 删除数据行时，将行ID发送到后台，后台在数据库中删除，数据库删除成功后，在页面DOM中将数据行也删除

### 2.Ajax 应用场景
#### (1)百度搜索引擎
![avatar](/day14/imgs/131.png)

当我们在百度中输入一个“老”字后，会马上出现一个下拉列表！列表中显示的是包含“传”字的4个关键字。

其实这里就使用了AJAX技术！当文件框发生了输入变化时，浏览器会使用AJAX技术向服务器发送一个请求，查询包含“传”字的前10个关键字，然后服务器会把查询到的结果响应给浏览器，最后浏览器把这4个关键字显示在下拉列表中。

- 整个过程中页面没有刷新，只是刷新页面中的局部位置而已！
- 当请求发出后，浏览器还可以进行其他操作，无需等待服务器的响应！
#### (2)用户注册异步检测用户名是否存在
![avatar](/day14/imgs/142.png)

当输入用户名后，把光标移动到其他表单项上时，浏览器会使用AJAX技术向服务器发出请求，服务器会查询名为zhangSan的用户是否存在，最终服务器返回true表示名为lemontree7777777的用户已经存在了，浏览器在得到结果后显示“用户名已被注册！”。

- 整个过程中页面没有刷新，只是局部刷新了；
- 在请求发出后，浏览器不用等待服务器响应结果就可以进行其他操作；

### 3.Ajax 优缺点
**优点**：
- AJAX使用Javascript技术向服务器发送异步请求；
- AJAX无须刷新整个页面；
- 因为服务器响应内容不再是整个页面，而是页面中的局部，所以AJAX性能高；

**缺点**：
- AJAX并不适合所有场景，很多时候还是要使用同步交互；
- AJAX虽然提高了用户体验，但无形中向服务器发送的请求次数增多了，导致服务器压力增大；
- 因为AJAX是在浏览器中使用Javascript技术完成的，所以还需要处理浏览器兼容性问题；

### 4.原生Ajax 技术
**四步操作**
- 创建核心对象；
- 使用核心对象打开与服务器的连接；
- 发送请求
- 注册监听，监听服务器响应。
**XMLHTTPRequest**
- open(请求方式, URL, 是否异步)
- send(请求体)
- onreadystatechange，指定监听函数，它会在xmlHttp对象的状态发生变化时被调用
- readyState，当前xmlHttp对象的状态，其中4状态表示服务器响应结束
- status：服务器响应的状态码，只有服务器响应结束时才有这个东东，200表示响应成功；
- responseText：获取服务器的响应体

底层Ajax是通过 XMLHTTPRequest 对象实现

[原生Ajax实现](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/SourceAjax.md")

### 5.Jquery Ajax 技术

jQuery其实就是一个JavaScript的类库，其将复杂的功能做了上层封装，使得开发者可以在其基础上写更少的代码实现更多的功能

jQuery Ajax本质 XMLHttpRequest 或 ActiveXObject 

[Jquery Ajax](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/JqueryAjax.md)

### 6.跨域请求
#### (1)同源策略机制
浏览器有一个很重要的概念——同源策略(Same-Origin Policy)。所谓同源是指，域名，协议，端口相同。不同源的客户端脚本(javascript、ActionScript)在没明确授权的情况下，不能读写对方的资源。

简单的来说，浏览器允许包含在页面A的脚本访问第二个页面B的数据资源，这一切是建立在A和B页面是同源的基础上。

如果Web世界没有同源策略，当你登录淘宝账号并打开另一个站点时，这个站点上的JavaScript可以跨域读取你的淘宝账号数据，这样整个Web世界就无隐私可言了。
#### (2)JSONP JS AND AJAX 解决跨域
JSONP是JSON with Padding的略称。可以让网页从别的域名（网站）那获取资料，即跨域读取数据。

[Jquery JS and Ajax](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/JsonpAjax.md)

#### (3)CORS 解决跨域

随着技术的发展，现在的浏览器可以支持主动设置从而允许跨域请求，即：跨域资源共享（CORS，Cross-Origin Resource Sharing），其本质是设置响应头，使得浏览器允许跨域请求。

**简单请求 OR 非简单请求**
```
条件：
    1、请求方式：HEAD、GET、POST
    2、请求头信息：
        Accept
        Accept-Language
        Content-Language
        Last-Event-ID
        Content-Type 对应的值是以下三个中的任意一个
                                application/x-www-form-urlencoded
                                multipart/form-data
                                text/plain
  
注意：同时满足以上两个条件时，则是简单请求，否则为复杂请求
```
**简单请求和非简单请求的区别？**
```
简单请求：一次请求
非简单请求：两次请求，在发送数据之前会先发一次请求用于做“预检”，只有“预检”通过后才再发送一次请求用于数据传输。
```
**关于“预检”**
```
- 请求方式：OPTIONS
- “预检”其实做检查，检查如果通过则允许传输数据，检查不通过则不再发送真正想要发送的消息
- 如何“预检”
     => 如果复杂请求是PUT等请求，则服务端需要设置允许某请求，否则“预检”不通过
        Access-Control-Request-Method
     => 如果复杂请求设置了请求头，则服务端需要设置允许某请求头，否则“预检”不通过
        Access-Control-Request-Headers
```
**基于cors实现AJAX请求:**

1.支持跨域，简单请求

服务器设置响应头：Access-Control-Allow-Origin = '域名' 或 '*'

[支持跨域，简单请求](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/jiandanajaxcors.md)

2.支持跨域，复杂请求

由于复杂请求时，首先会发送“预检”请求，如果“预检”成功，则发送真实数据。
- “预检”请求时，允许请求方式则需服务器设置响应头：Access-Control-Request-Method
- “预检”请求时，允许请求头则需服务器设置响应头：Access-Control-Request-Headers
- “预检”缓存时间，服务器设置响应头：Access-Control-Max-Age

[支持跨域，复杂请求](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/fuzaajaxcors.md)

3.跨域获取响应头

默认获取到的所有响应头只有基本信息，如果想要获取自定义的响应头，则需要再服务器端设置Access-Control-Expose-Headers。

[跨域获取响应头](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/ajaxhuoquheader.md)

4.跨域传输cookie

在跨域请求中，默认情况下，HTTP Authentication信息，Cookie头以及用户的SSL证书无论在预检请求中或是在实际请求都是不会被发送。

如果想要发送：
- 浏览器端：XMLHttpRequest的withCredentials为true
- 服务器端：Access-Control-Allow-Credentials为true
- 注意：服务器端响应的 Access-Control-Allow-Origin 不能是通配符 *

[跨域传输cookie](https://github.com/xiaozhiqi2000/learn_django/blob/master/day14/ajaxchuanchucookie.md)


## 三、实例
本地域名请求实例

HTML
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ajax请求</title>
</head>
<body>
    <div>
        <p>用户名:<input type="text" id="username"/></p>
    </div>
    <div>
        <p>密码:<input type="password" id="pwd"/></p>
    </div>
    <input type="button" value="提交" onclick="SubmitForm();"/>

    <script src="/static/jquery-1.12.4.js"></script>
    <script>
        function SubmitForm() {
            $.ajax({
                url:'/web/',
                type:'POST',
                data:{'user':$('#username').val(),'pwd':$('#pwd').val()},
                dataType:'json',
                success:function (data) {
                    // data = 字符串 '{'status':xxx,'message':xxx}'
                    // var data_dict = JSON.parse(data) 将字符串格式的字典转换为字典
                    // 如果上面一步没写，则需要写dataType:'json',
                    if(data.status){
                        location.href = 'http://www.baidu.com';
                    }else{
                        alert(data.message);
                    }
                }
            })
        }
    </script>
</body>
</html>
```
urls
```
from django.conf.urls import url,include
from django.contrib import admin
from ajax import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^web/', views.ajax_demo),
]
```
views
```
from django.shortcuts import render,HttpResponse,redirect

import json

def ajax_demo(request):
    if request.method == 'POST':
        ret = {'status':False,'message':''}
        user = request.POST.get('user',None)
        pwd = request.POST.get('pwd',None)
        if user == 'tom' and pwd == '123':
            ret['status'] = True
            return HttpResponse(json.dumps(ret))
        else:
            ret['message'] = '用户名或密码错误'
            return HttpResponse(json.dumps(ret))

    return render(request,'ajax_demo.html')
```






