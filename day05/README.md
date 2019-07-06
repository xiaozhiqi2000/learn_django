# 今天主要内容
[django Views视图函数]()

参考：

[Django1.11 官网HttpResponse](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/)

[Django1.11 官网Response与Request](https://docs.djangoproject.com/en/1.11/ref/request-response/)


## views中两个核心对象
![avatar](/day05/imgs/51.png)

http请求中产生两个核心对象：
- http请求：HttpRequest对象
- http响应：HttpResponse对象

### 1.HttpRequest对象
- HttpRequest属性
```
path：      请求页面的全路径，不包括域名
method：    请求中使用的HTTP方法的字符串表示。全大写表示。例如req.method=="GET",req.method=="POST":
FILES：     包含所有上传文件的类字典对象；FILES中的每一个Key都是<input type="file" name="" />标签中
            name属性的值，FILES中的每一个value同时也是一个标准的python字典对象，包含下面三个Keys：
                filename：      上传文件名，用字符串表示
                content_type:   上传文件的Content Type
                content：       上传文件的原始内容
user：      是一个django.contrib.auth.models.User对象，代表当前登陆的用户。如果访问用户当前
            没有登陆，user将被初始化为django.contrib.auth.models.AnonymousUser的实例。你
            可以通过user的is_authenticated()方法来辨别用户是否登陆：
            if req.user.is_authenticated();只有激活Django中的AuthenticationMiddleware
            时该属性才可用

session：   唯一可读写的属性，代表当前会话的字典对象；自己有激活Django中的session支持时该属性才可用。
COOKIES:    包含所有cookies的标准Python字典对象；keys和values都是字符串。
raw_post_data:  原始HTTP POST数据，未解析过。高级处理时会有用处。
```
- HttpRequest方法
```
get_full_path()：返回包含查询字符串的请求路径。例如， "/music/bands/the_beatles/?print=true"
```

### 2.HttpResponse对象
对于HttpRequest 对象来说，是由Django自动创建, 但是，HttpResponse对象就必须我们自己创建。

每个View请求处理方法必须返回一个HttpResponse对象。如果没有返回，则会捕获valueerror异常，HttpResponse类在django.http.HttpResponse

#### 构造HttpResponse
在HttpResponse对象上常用方法：HttpResponse()、render()、render_to_response()、redirect(重定向)

- render与render_to_response区别在于第一个参数是否要request，所以就用render
- 表单提交的时候render_to_response还需要添加 context_instance=RequestContext(request)否则会报csrf错误
```
HttpResponse("Here's the text of the Web page.")
HttpResponse("Text only, please.", mimetype="text/plain")

render(request,'index.html',{向模板传递的变量})

render_to_response('index.html',{向模板传递的变量})

redirect("http://www.baidu.com")  或者 redirect("/blog/py/login")
```

#### locals()
可以直接将函数中所有的变量全部传给模板，自动拼接成字典，很方便。

但是它会多传递一些没用的变量，有点浪费
