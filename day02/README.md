# 今天主要内容
1. [django 概述]()
2. [django 安装]()
3. [django 常用命令]()
4. [django 项目创建]()

## 一、概述
### 1.什么是框架
框架，即framework，特指为解决一个开放性问题而设计的具有一定约束性的支撑结构，使用框架可以帮你快速开发特定的系统，简单说就是使用别人搭好的舞台，你来做表演

### 2.常见的python web框架
- Full-Stack Frameworks（全栈框架、重量级框架）：
Django、web2py、TurboGears、Pylons、...

- Non Full-Stack Frameworks（非全栈框架、轻量级的框架）：
tornado、Flask、Bottle、web.py、Pyramid、...

[详见python官网有哪些框架](https://wiki.python.org/moin/WebFrameworks)

### 3.如何选择框架
- 根据项目需求去选择。
- 根据框架的特点去选择

国内常用：django、tornado、flask、bottle，Django相较与其他WEB框架其优势为：大而全，框架本身集成了ORM、模型绑定、模板引擎、缓存、Session等诸多功能。

[Django1.11官网](https://docs.djangoproject.com/en/1.11/)

## 二、安装
使用pip安装或者pycharm安装都可以
```
pip install django==1.11.15 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

```

## 三、常用命令
python manage.py 直接执行会打印全部命令
```
django-admin startproject sitename       #创建一个项目叫sitename
django-admin startapp appname            #创建一个app叫appname
python manage.py makemigrations          #app目录下创建migrations目录，并记录下你所有关于models.py的改动
python manage.py migrate                 #将migrations目录的.py在数据库中创建表修改表等等操作
python manage.py flush                   #清空数据库
python manage.py runserver 0.0.0.0:8000  #启动wsgi,打开浏览器即可访问你的IP:8000
python manage.py shell                   #shell里面调用当前项目的models.py中的API，对于操作数据，还有一些小测试非常方便
python manage.py createsuperuser         #django默认是有个后台,在urls已经配置,这个是创建后台用户
python manage.py changepassword          #django默认后台用户的密码
python manage.py clearsessions           #清除会话
```

## 四、创建项目查看目录结构
- static是自己创建的目录用于放置js,css,image等等，需要settings中配置
- upload是自己创建的目录用于图片上传,需要在settings中配置
```
(py36) [root@localhost ~]# django-admin startproject mysite
(py36) [root@localhost ~]# tree mysite
mysite
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

(py36) [root@localhost ~]# mkdir -p mysite/{blog,static,upload}
(py36) [root@localhost ~]# django-admin startapp blog mysite/blog
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
