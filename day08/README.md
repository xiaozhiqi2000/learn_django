# 今天主要内容
[django Models实例操作]()

## 一、表模型剖析实例
#### 1.实例：我们来假定下面这些概念，字段和关系

- 作者模型表：一个作者有姓名。
- 作者详细模型表：把作者的详情放到详情表，包含性别，email地址和出生日期，作者详情模型和作者模型之间是一对一的关系（one－to－one）（类似于每个人和他的身份证之间的关系），在大多数情况下我们没
有必要将他们拆分成两张表，这里只是引出一对一的概念。
- 出版商模型表：出版商有名称，地址，所在城市，省，国家和网站。
- 书籍模型表：书籍有书名和出版日期，一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系就是多对多的关联关系（many－to－many），一本书只应该由一个出版商出版，所以出版商和书>籍是一对多关联关系（one－to－many），也被称作外键。

#### 2.models设置
```
from django.db import models

class Publisher(models.Model):    
    name = models.CharField(max_length=30, verbose_name="名称")
    address = models.CharField("地址", max_length=50)    
    city = models.CharField('城市',max_length=60)    
    state_province = models.CharField(max_length=30)    
    country = models.CharField(max_length=50)    
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
    sex = models.BooleanField(max_length=1, choices=((0, '男'),(1, '女'),))
    email = models.EmailField()
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    author = models.OneToOneField(Author)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2,default=10)

    def __str__(self):
        return self.title
```
#### 3.分析代码
- 1.每个数据模型都是django.db.models.Model的子类，它的父类Model包含了所有必要的和数据库交互的方法。并提供了一个简介漂亮的定义数据库字段的语法。
- 2.每个模型相当于单个数据库表（多对多关系例外，会多生成一张关系表），每个属性也是这个表中的字段。属性名就是字段名，它的类型（例如CharField）相当于数据库的字段类型（例如varchar）。大家可以留意下其它的类型都和数据库里的什么字段对应。
- 3.模型之间的三种关系：一对一，一对多，多对多。
   - 一对一：实质就是在主外键（author_id就是foreign key）的关系基础上，给外键加了一个UNIQUE＝True的属性；
   - 一对多：就是主外键关系；（foreign key）
   - 多对多：(ManyToManyField) 自动创建第三张表(当然我们也可以自己创建第三张表：两个foreign key)
