# 今天主要内容
[django Template]()

参考：

[Django1.11 官网Tempaltes](https://docs.djangoproject.com/en/1.11/ref/templates/)

[Django1.11 官网模板语言](https://docs.djangoproject.com/en/1.11/ref/templates/language/#templates)

#![avatar](/day05/imgs/51.png)

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
