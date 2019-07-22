# 今天主要内容

参考:

[Django1.11 分页pageination ](https://docs.djangoproject.com/en/1.11/topics/pagination/)

## 一、Django 内置分页
views.py
```
rom django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})
```
list.html
```
{% for contact in contacts %}
    {# Each "contact" is a Contact model object. #}
    {{ contact.full_name|upper }}<br />
    ...
{% endfor %}

<div class="pagination">
    <span class="step-links">
        {% if contacts.has_previous %}
            <a href="?page={{ contacts.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ contacts.number }} of {{ contacts.paginator.num_pages }}.
        </span>

        {% if contacts.has_next %}
            <a href="?page={{ contacts.next_page_number }}">next</a>
        {% endif %}
    </span>
</div>
```

## 二、自定义分页
分页功能在每个网站都是必要的，对于分页来说，其实就是根据用户的输入计算出应该在数据库表中的起始位置。

1.设定每页显示数据条数
2.用户输入页码（第一页、第二页...）
3.设定显示多少页号
4.获取当前数据总条数
5.根据设定显示多少页号和数据总条数计算出，总页数
6.根据设定的每页显示条数和当前页码，计算出需要取数据表的起始位置
7.在数据表中根据起始位置取值，页面上输出数据
8.输出分页html，如：［上一页］［1］［2］［3］［4］［5］［下一页］

urls.py
```
from django.conf.urls import url,include
from django.contrib import admin
from app02.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^page/', page),
]
```
models.py
```
from django.db import models

# Create your models here.

class HostInfo(models.Model):

    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
```
views.py
```
from django.shortcuts import render,render_to_response,redirect
from django.utils.safestring import mark_safe
from app02 import models

def try_int(arg,default):

    try:
        arg = int(arg)
    except Exception:
        arg = default
    return arg


class PageInfo():

    def __init__(self,current_page,all_count,per_item=10):
        self.CurrentPage = current_page
        self.AllCount = all_count
        self.PerItem = per_item

    @property
    def start(self):
        return (self.CurrentPage-1)*self.PerItem

    @property
    def end(self):
        return self.CurrentPage*self.PerItem

    @property
    def all_page_count(self):
        temp = divmod(self.AllCount, self.PerItem)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        return all_page_count

def Pager(page,all_page_count):
    '''
    page:当前页
    all_page_count:所有页
    '''
    page_html = []

    first_html = "<a href='/page?p=%d'>首页</a>" %(1,)
    page_html.append(first_html)


    if page <= 1:
        prv_html = "<a href='#'>上一页</a>"
    else:
        prv_html = "<a href='/page?p=%d'>上一页</a>" %(page-1,)
    page_html.append(prv_html)

    begin = 0
    end =0

    if all_page_count <= 11:
        begin = 0
        end = all_page_count
    else:
        if page < 6:
            begin = 0
            end = 11
        else:
            if page + 6 > all_page_count:
                begin = page - 6
                end = all_page_count
                if end > all_page_count:
                    end = all_page_count
            else:
                begin = page - 6
                end = page + 6


    for i in range(begin+1,end+1):
        if page == i:
            a_html = "<a class='active' href='/page?p=%d'>%d</a>"  %(i,i)
        #mark_safe让他转义为html
        else:
            a_html = "<a href='/page?p=%d'>%d</a>"  %(i,i)
        page_html.append(a_html)


    if page >= all_page_count:
        next_html = "<a href='#'>下一页</a>"
    else:
        next_html = "<a href='/page?p=%d'>下一页</a>" %(page+1,)
    page_html.append(next_html)



    end_html = "<a href='/page?p=%d'>尾页</a>" %(all_page_count,)
    page_html.append(end_html)

    page_string = mark_safe(''.join(page_html))

    return page_string



def page(request):
    page = request.GET.get('p',1)
    page = try_int(page, 1)
    count = models.HostInfo.objects.all().count()

    pageObj = PageInfo(page,count)
    result = models.HostInfo.objects.all()[pageObj.start:pageObj.end]

    page_string = Pager(page, pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    return render_to_response('page.html',ret)
```
page.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .pager a{
            display: inline-block;
            padding:5px;
            background-color: cadetblue;
            margin: 2px;
        }
        .pager a.active{
            background-color: chartreuse;
        }
    </style>
</head>
<body>
    <table border="1">

            <tr>
                <th>主机名</th>
                <th>IP</th>
            </tr>
            {% for i in data %}
            <tr>
                <td>{{ i.hostname }}</td>
                <td>{{ i.ip}}</td>
            </tr>
            {% endfor %}
    </table>
    <div>
        总共：{{ count }}页
    </div>
    <div class="pager">
        {{ page }}
    </div>
</body>
</html>
```
总结，分页时需要做三件事：
- 创建处理分页数据的类
- 根据分页数据获取数据
- 输出分页HTML，即：［上一页］［1］［2］［3］［4］［5］［下一页］
