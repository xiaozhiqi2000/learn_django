# 今天主要内容
1. [Web框架本质]()
2. [WSGI]()
3. [自定义Web框架]()
4. [MVC与MTV]()
3. [自定义Web框架]()

## 一、Web框架本质
对于所有的Web应用，本质上其实就是一个socket服务端，用户的浏览器其实就是一个socket客户端
```
#!/usr/bin/env python
#coding:utf-8
   
import socket
   
def handle_request(client):
    buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n\r\n")
    client.send("Hello, Seven")
   
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',8000))
    sock.listen(5)
   
    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()
   
if __name__ == '__main__':
    main()
```
通过socket来实现了其本质，而对于真实开发中的python web程序来说，一般会分为两部分：服务器程序和应用程序。
- 服务器程序负责对socket服务器进行封装，并在请求到来时，对请求的各种数据进行整理。
- 应用程序则负责具体的逻辑处理。为了方便应用程序的开发，就出现了众多的Web框架，例如：Django、Flask、web.py 等。

不同的框架有不同的开发方式，但是无论如何，开发出的应用程序都要和服务器程序配合，才能为用户提供服务。这样，服务器程序就需要为不同的框架提供不同的支持。这样混乱的局面无论对于服务器还是框架，都是不好的。对服务器来说，需要支持各种不同框架，对框架来说，只有支持它的服务器才能被开发出的应用使用。这时候，标准化就变得尤为重要。我们可以设立一个标准，只要服务器程序支持这个标准，框架也支持这个标准，那么他们就可以配合使用。一旦标准确定，双方各自实现。这样，服务器可以支持更多支持标准的框架，框架也可以使用更多支持标准的服务器。

## 二、WSGI
WSGI（Web Server Gateway Interface）是一种规范，它定义了使用python编写的web app与web server之间接口格式，实现web app与web server间的解耦
python标准库提供的独立WSGI服务器称为wsgiref。当还有其他的接口格式：
```bash
'cgi': CGIServer,
'flup': FlupFCGIServer,
'wsgiref': WSGIRefServer,
'waitress': WaitressServer,
'cherrypy': CherryPyServer,
'paste': PasteServer,
'fapws3': FapwsServer,
'tornado': TornadoServer,
'gae': AppEngineServer,
'twisted': TwistedServer,
'diesel': DieselServer,
'meinheld': MeinheldServer,
'gunicorn': GunicornServer,
'eventlet': EventletServer,
'gevent': GeventServer,
'geventSocketIO':GeventSocketIOServer,
'rocket': RocketServer,
'bjoern' : BjoernServer,
'auto': AutoServer,
```
Django如何实现WSGI，其实也是通过wsgiref模板来实现:
```
from wsgiref.simple_server import make_server
  
def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello world!</h1>'
  
if __name__ == '__main__':
    httpd = make_server('', 8000, RunServer)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
```

## 三、自定义Web框架
1. 通过 wsgiref 模板开发自己的 server
2. 对于login、index返回给用户浏览器一个简单的字符串，在现实的Web请求中一般会返回一个复杂的符合HTML规则的字符串，所以我们一般将要返回给用户的HTML写在指定文件中，然后再返回
3. 对于index1 遵循jinja2的语法规则，其内部会对指定的语法进行相应的替换，从而达到动态的返回内容，对于模板引擎的本质

```
from wsgiref.simple_server import make_server
from jinja2 import Template
  
def index():
    f = open('index.html')
    result = f.read()
    return result
  
def index1():
    '''这里使用template将变量传递给html'''
    f = open('index1.html')
    result = f.read()
    template = Template(result)
    data = template.render(name='John Doe', user_list=['alex', 'eric'])
    return data.encode('utf-8')
  
def login():
    f = open('login.html')
    data = f.read()
    return data
  
def routers():
    '''定义路由和处理的函数'''
    urlpatterns = (
        ('/index/', index),
        ('/index1/', index1),
        ('/login/', login),
    )
  
    return urlpatterns
  
  
def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    url = environ['PATH_INFO']
    urlpatterns = routers()
    func = None
    for item in urlpatterns:
        if item[0] == url:
            func = item[1]
            break
    if func:
        return func()
    else:
        return '404 not found'
  
if __name__ == '__main__':
    httpd = make_server('', 8000, run_server)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
```

## 四、MVC与MTV
### 1. MVC模式
![avatar](/day01/imgs/1.png)

所谓MVC就是把Web应用分为模型(M)，控制器(C)和视图(V)三层，他们之间以一种插件式的、松耦合的方式连接在一起:
- M 模型(Model)：负责业务对象与数据库的映射(ORM)
- V 视图(View)：负责与用户的交互(页面)
- C 控制器(Contorler)：接受用户的输入调用模型和视图完成用户的请求

### 2. MTV模式
![avatar](/day01/imgs/4.jpg)

Django的MTV模式本质上和MVC是一样的，也是为了各组件间保持松耦合关系，只是定义上有些许不同
Django的MTV分别是值：
- M 代表模型(Model)：负责业务对象和数据库的关系映射(ORM)。
- T 代表模板(Template)：负责如何把页面展示给用户(html)。
- V 代表视图(View)：负责业务逻辑，并在适当时候调用Model和Template。

除了以上三层之外，还需要一个URL分发器，它的作用是将一个个URL的页面请求分发给不同的View处理，View再调用相应的Model和Template，MTV的响应模式如下所示：

![avatar](/day01/imgs/3.png)

1. Web服务器（中间件）收到一个http请求
2. Django在URLconf里查找对应的视图(View)函数来处理http请求
3. 视图函数调用相应的数据模型来存取数据、调用相应的模板向用户展示页面
4. 视图函数处理结束后返回一个http的响应给Web服务器
5. Web服务器将响应发送给客户端
