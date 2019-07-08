# 今天主要内容
[django Model(三)实例操作]()

## 实例操作
### 1.查看mysite1/app01/models.py
- 作者模型表Author：一个作者有姓名。
- 作者详细模型表AuthorDetail：把作者的详情放到详情表，包含性别，email地址和出生日期，作者详情模型和作者模型之间是一对一的关系（one－to－one）（类似于每个人和他的身份证之间的关系），在大多数情况下我们没 有必要将他们拆分成两张表，这里只是引出一对一的概念。
- 出版商模型表Publisher：出版商有名称，地址，所在城市，省，国家和网站。
- 书籍模型表Book：书籍有书名和出版日期，一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系就是多对多的关联关系（many－to－many），一本书只应该由一个出版商出版，所以出版商和书籍是一对多关联关系（one－to－many），也被称作外键。

同步数据库
```
python manage.py makemigrations
python manage.py migrate
```
### 2.查看mysite1/urls.py
- add 批量创建数据
- danbiao 单表查询数据
- yiduiyi 一对一查询数据
- yiduiduo 一对多查询数据
- duoduiduo 多对多查询数据
```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add/', views.addata),
    url(r'^danbiao/', views.danbiao),
    url(r'^yiduiyi/', views.yiduiyi),
    url(r'^yiduiduo/', views.yiduiduo),
    url(r'^duoduiduo/', views.duoduiduo),
]
```
### 3.查看mysite1/app01/views.py
#### (1) 批量创建数据
```
python manage.py runserver 8080
浏览器访问 http://127.0.0.1:8080/add
```
#### (2) 进入Django shell环境
```
python manage.py shell   # 进入django的shell

from app01 import models # 导入models模块
```
#### (3) 单表查询
```
# 获取所有用户的名字
authorall = models.Author.objects.all()
print(authorall.query)

# 获取名字是ShiZhongyu这个用户
queryset = models.Author.objects.filter(name='ShiZhongyu')
print(queryset.query)
print(type(queryset))
for item in queryset:
    print(item.name)
    print(item.address)

# get是userinfo类 model 对象,不需要迭代取值,直接取,
obj = models.Author.objects.get(id=10)
print(type(obj))
print(obj)  # 会自动执行UserInfo中__str__方法打印self.name所以是id=10的name
print(obj.id)
print(obj.name)
```
