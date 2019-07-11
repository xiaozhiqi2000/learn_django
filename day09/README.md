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
#### (3) 单表查询、一对多查询、多对多查询、对象式查询、双下划线查询
```
#--------------------对象形式的查找--------------------------
# 正向查找
      ret1=models.Book.objects.first()
      print(ret1.title)
      print(ret1.price)
      print(ret1.publisher)
      print(ret1.publisher.name)  #因为一对多的关系所以ret1.publisher是一个对象,而不是一个queryset集合

# 反向查找
      ret2=models.Publisher.objects.last()
      print(ret2.name)
      print(ret2.city)
      #如何拿到与它绑定的Book对象呢?
      print(ret2.book_set.all()) #ret2.book_set是一个queryset集合

#---------------了不起的双下划线(__)之单表条件查询----------------

      models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值
    
      models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
      models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in
    
      models.Tb1.objects.filter(name__contains="ven")
      models.Tb1.objects.filter(name__icontains="ven") # icontains大小写不敏感
    
      models.Tb1.objects.filter(id__range=[1, 2])   # 范围bettwen and
    
      startswith，istartswith, endswith, iendswith,

#----------------了不起的双下划线(__)之多表条件关联查询---------------

# 正向查找(条件)

      #ret3=models.Book.objects.filter(title='Python').values('id')
      #print(ret3)#[{'id': 1}]

      #正向查找(条件)之一对多

      ret4=models.Book.objects.filter(title='Python').values('publisher__city')
      print(ret4)  #[{'publisher__city': '北京'}]

      #正向查找(条件)之多对多
      ret5=models.Book.objects.filter(title='Python').values('author__name')
      print(ret5)
      ret6=models.Book.objects.filter(author__name="alex").values('title')
      print(ret6)

      #注意
      #正向查找的publisher__city或者author__name中的publisher,author是book表中绑定的字段
      #一对多和多对多在这里用法没区别

# 反向查找(条件)

      #反向查找之一对多:
      ret8=models.Publisher.objects.filter(book__title='Python').values('name')
      print(ret8)  #[{'name': '人大出版社'}]  注意,book__title中的book就是Publisher的关联表名

      ret9=models.Publisher.objects.filter(book__title='Python').values('book__authors')
      print(ret9)  #[{'book__authors': 1}, {'book__authors': 2}]

      #反向查找之多对多:
      ret10=models.Author.objects.filter(book__title='Python').values('name')
      print(ret10) #[{'name': 'alex'}, {'name': 'alvin'}]

      #注意
      #正向查找的book__title中的book是表名Book
      #一对多和多对多在这里用法没区别
```
#### 总结
1.对象式查询必须是单个对象，不能为QuerySet对象，可以加个fist()或者[0]，取第一个对象，如models.AuthorDetail.objcts.all()[0].author.name，适用一对多，多对多
2.对象式反向查询也是要单个对象，通过该对象.关联表_set取到关联表的对象，如models.Publisher.objects.filter(id=1)[0].book_set.first().title，适用一对多，多对多
3.双下划线条件查询：(1)通过约束条件对应的字段__关联表的字段名来查找条件，(2)通过对应表名__字段名来查找条件
- publisher = models.ForeignKey(Publisher), models.Book.objects.filter(publisher__name="人民出版社").values("publisher__address")
- authors = models.ManyToManyField(Author), models.Book.objects.filter(authors__name="MaChao").values("publisher__name")
- models.Publisher.objects.filter(book__title="Go核心编程").values("name")
