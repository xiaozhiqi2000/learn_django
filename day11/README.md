# 今天主要内容
[django Model Admin]()
参考：

[Django1.11 官网 Admin](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/)

## 一、Admin 概述
django amdin是django提供的一个后台管理数据库的页面，管理页面提供完善的html和css，使得你在通过Model创建完数据库表之后，就可以对数据进行增删改查，步骤:
- 先同步数据库
- 创建后台管理员
- 配置url
- 注册和配置django admin后台管理页面

一些常用的设置技巧：
- list_display：指定要显示的字段
- search_fields：指定搜索的字段
- list_filter：指定列表过滤器
- ordering：指定排序字段
- fields\exclude：指定编辑表单需要编辑\不需编辑的字段
- fieldsets：设置分组表单
- filter_horizontal：指定多对多选择
- raw_id_fields：一对多选择

## 二、Amin 配置步骤
这里使用day09使用的model及作者,作者详情,出版社,书籍 四者关系
#### 1. 配置后台管理的url，默认已经设置好
```
url(r'^admin/', include(admin.site.urls))
```
#### 2. 同步数据库，创建admin需要的表
```
python manage.py makemigrations
python manage.py migrate
```
#### 3. 创建admin后台管理员帐号密码
```
python manage.py createsuperuser

#修改管理员密码
python manage.py changepassword
```
#### 4. 设置数据库表
```
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30, verbose_name="出版社名称")
    address = models.CharField("地址", max_length=50)
    city = models.CharField("城市", max_length=60)
    state_province = models.CharField("省份", max_length=30)
    country = models.CharField("国家", max_length=50)
    website = models.URLField()

    class Meta:
        verbose_name = '出版商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class AuthorDetail(models.Model):
    sex = models.BooleanField(max_length=1, choices=((0, '男'), (1, '女'),))
    email = models.EmailField()
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    author = models.OneToOneField(Author)


class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    publisher = models.ForeignKey(Publisher)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title
```
#### 5. 设置admin.py
```
from django.contrib import admin
from app01 import models

# @admin.register(Author)#----->单给某个表加一个定制,就不不需要后面的admin.site.register(defindAdminAuthor,Author)
class defindAdminAuthor(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)
    search_fields = ('name',)

class defindAdminAuthorDetail(admin.ModelAdmin):
    list_display = ('id', 'sex', 'email', 'email', 'address', 'birthday')
    ordering = ('id',)


class defindAdminPublisher(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'city', 'state_province', 'country', 'website')
    ordering = ('id',)
    search_fields = ('name',)

class defindAdminBook(admin.ModelAdmin):
    """
    多对多的字段是不能显示的
    """
    list_display = ('id', 'title', 'publication_date', 'price', 'publisher',)
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('publisher',)

#将models中的类名和对应admin的类名注册到admin表中
admin.site.register(models.Author, defindAdminAuthor)
admin.site.register(models.AuthorDetail, defindAdminAuthorDetail)
admin.site.register(models.Publisher, defindAdminPublisher)
admin.site.register(models.Book, defindAdminBook)
```
#### 6.如图
![avatar](/day11/imgs/11.png)
#### 7.如果你觉得英文界面不好用，可以在setting.py 文件中修改以下选项
```
LANGUAGE_CODE = 'en-us'  #LANGUAGE_CODE = 'zh-hans'
```

## 三、Admin 总结
Django admin后台管理不是必要的，方便是方便，当然玩的6也不错

没有admin 通过 url views modes tempalte 自己可以玩
















