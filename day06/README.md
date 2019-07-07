# 今天主要内容
[django Template]()

参考：

[Django1.11 官网Tempaltes](https://docs.djangoproject.com/en/1.11/ref/templates/)

[Django1.11 官网模板语言](https://docs.djangoproject.com/en/1.11/ref/templates/language/#templates)


## 一、Django如何执行
```
return render(request,"index.html",{"name":"alex"})
 
# "index.html是Template模板
# {"name":"alex"}是上下文
```

Django是HttpResponse如何将template,context封装到render中
### 手动嵌套变量到模板中
```
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
```
### django通过模板语言将变量嵌套html中(一)
```
from django import template
t = template.Template('My name is {{ name }}.')
c = template.Context({'name': 'Adrian'})
print(t.render(c))
```
### django通过模板语言将变量嵌套html中(二)
```
import datetime
from django import template
import DjangoDemo.settings
 
now = datetime.datetime.now()
fp = open(settings.BASE_DIR+'/templates/Home/Index.html')
t = template.Template(fp.read())
fp.close()
html = t.render(template.Context({'current_date': now}))
return HttpResponse(html)
```
### django通过模板语言将变量嵌套html中(三)
```
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime
 
def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
```
## 二、模板语言
#### 1.模板变量
```
{{ var_name }}
```
#### 2.模板取值
```
# views函数返回的是字符串,通过{{ k1 }}获取字符串v1,前端引用的名字是k1
return render('index.html',{'k1':'v1'}
 
# views函数返回的是列表,通过{{ list.0 }}获取字符串11,{{ list.1 }}获取字符串22,前端引用的名字是list
return render('index.html',{'list':[11,22,33,44]}
 
# views函数返回的是字典,通过{{ dict.k1 }}获取字符串v1,{{ dict.k2 }}获取字符串v2,前端引用的名字是dict
return render('index.html',{'dict':{'k1':'v1','k2':'v2'}}
 
# views把全部变量传入前端，locals(),前端引用的名字直接是views中的变量名
return render('index.html',locals()}
 
# views把一个对象传入前端，前端通过obj.name,obj.age来取值
def index(request):
    class Person():
        def __init__(self,name,age):
             self.name = name
             self.age = age
    s4 = Person("xiao",18)
    return render(request,"index.html",{"obj":s4})
```
#### 3.流程控制
```
{% if a > b %}
    .......
{% elif a == b %}
    .......
{% else %}
    .......
{% endif %}
```
#### 4.流程控制
```
{% for item in data %}
　　{{ item }}<br>
   {# 下面几个是特殊变量 #}
   forloop.counter   {# 索引从1开始 #}
   forloop.counter0  {# 索引从0开始 #}
   forloop.first     {# 是否是循环的第一个 #}
   forloop.last      {# 是否是循环的最后一个 #}
{% endfor %}
```
#### 5.更多常用标签
```
01、{% if %}
    可以使用and, or, not来组织你的逻辑。但不允许and和or同时出现的条件语句中。新版本中已经支持{% elif %}这样的用法。
02、{% ifequal %}和{% ifnotequal %}
    比较是否相等，只限于简单的类型，比如字符串，整数，小数的比较，列表，字典，元组不支持。
03、{% for %}
    用来循环一个list，还可以使用resersed关键字来进行倒序遍历，一般可以用if语句来先判断一下列表是否为空，再进行遍历；还可以使用empty关键字来进行为空时候的跳转。
    
    ** for标签中可以使用forloop
    a. forloop.counter 当前循环计数，从1开始
    b. forloop.counter0 当前循环计数，从0开始，标准索引方式
    c. forloop.revcounter 当前循环的倒数计数，从列表长度开始
    d. forloop.revcounter0 当前循环的倒数计数，从列表长度减1开始，标准
    e. forloop.first bool值，判断是不是循环的第一个元素
    f. forloop.last 同上，判断是不是循环的最后一个元素
    g. forloop.parentloop 用在嵌套循环中，得到parent循环的引用，然后可以使用以上的参数
04、{% cycle %} 
    在循环时轮流使用给定的字符串列表中的值。
05、{# #} 单行注释，{% comment %}多行注释
06、{% csrf_token %}
    生成csrf_token的标签，用于防止跨站攻击验证。
07、{% debug %}
    调用调试信息
08、{% filter %}
    将filter 标签圈定的内容执行过滤器操作。
09、{% autoescape %}
    自动转义设置
10、{% firstof %}
    输出第一个值不等于False的变量
11、{% load %}
    加载标签库
12、{% now %}
    获取当前时间
13、{% spaceless %}
    移除空格
14、{% url %}
    引入路由配置的地址
15、{% verbatim %}
    禁止render
16、{% with %}
    用更简单的变量名缓存复杂的变量名
```
[Django官网更多内置标签](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)
#### 6.自定义方法filter或者simple_tag
filter和simple_tag的区别：
- filter：限制传参2个，支持 if 条件
- simple_tag：不限制传参，不支持 if 条件

1、在app01中创建templatetags模块(templatetags名字是不能变)

2、创建任意 .py 文件，如：mysimple.py
```
from django import template
from django.utils.safestring import mark_safe
    
register = template.Library() # 这一句一定是这样写的
    
@register.simple_tag 
def my_simple_time(v1,v2,v3):
'''传递多个参数'''
    return  v1 + v2 + v3
    
@register.simple_tag
def my_input(id,arg):
    result = "<input type='text' id='%s' class='%s' />" %(id,arg,)
    return mark_safe(result)
     
@register.filter
    def f1(value):
        return value + '1000'
         
@register.filter
def f2(value,arg):
'''传递一个参数'''
return value + '1000' + arg
 
@register.filter
def f3(value):
    if value == 'vvv':
        return True
    else:   
        return False
```
3、在使用自定义simple_tag的html文件中导入之前创建的 mysimple.py 文件名
```
{% load mysimple %}
```
4、使用simple_tag和filter,它们使用是不一样的
```
{% my_simple_time 1 2 3%}    # 可以传递多个参数
{% my_input 'id_username' 'hide'%}
{{ k1 | f1 }}
{{ k1 | f2:'python' }}       # 只能传递一个参数
{% if k1 | f3 %}
    <h1>True</h1>
{% else %}
    <h1>False</h1>
{% endif %}
```
5、在settings中配置当前app，不然django无法找到自定义的simple_tag　　
```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
)
```
## 三、模板继承
https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#extends

https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#block

https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#include
```
母板：{% block title %}{% endblock %}
子板：{% extends "base.html" %}
     　　{% include "xx.html" %}  # 在子板中使用其他模板
　　　{% block title %}{% endblock %}
```
查看当前：layout.html assets.html userinfo.html xx.html



































