# 今天主要内容
1. [Web框架本质]()
2. [WSGI]()
3. [自定义Web框架]()
4. [MVC与MTV]()
3. [自定义Web框架]()

## Web框架本质
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

## WSGI
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

## 自定义Web框架
### 1、框架
```
from wsgiref.simple_server import make_server
from jinja2 import Template
  
  
def index():
    # return 'index'
  
    # template = Template('Hello {{ name }}!')
    # result = template.render(name='John Doe')
  
    f = open('index.html')
    result = f.read()
    template = Template(result)
    data = template.render(name='John Doe', user_list=['alex', 'eric'])
    return data.encode('utf-8')
  
  
def login():
    # return 'login'
    f = open('login.html')
    data = f.read()
    return data
  
  
def routers():
  
    urlpatterns = (
        ('/index/', index),
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
### 3、模板引擎
```
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <h1>{{name}}</h1>

    <ul>
        {% for item in user_list %}
        <li>{{item}}</li>
        {% endfor %}
    </ul>

</body>
</html>
```

































## 变量
![avatar](/day01/imgs/1.png)

