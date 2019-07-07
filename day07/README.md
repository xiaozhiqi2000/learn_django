# 今天主要内容
[django Model模型]()

参考：

[Django1.11 官网Model](https://docs.djangoproject.com/en/1.11/topics/db/models/)


## 一、Django 数据库相关
### 1.Django支持哪些数据库
django默认支持sqlite、mysql、oracle、postgresql数据库，像db2和sqlserver之类的数据库需要第三方的支持。具体详见：

[Django1.11 官网Model](https://docs.djangoproject.com/en/1.11/ref/databases/)

### 2.Mysql有哪些驱动程序
```
MySQLdb（mysql-python）：https://pypi.python.org/pypi/MySQL-python/1.2.5（支持python2）
mysqlclient：https://pypi.python.org/pypi/mysqlclient （支持python3）
MySQL Connector/Python：  https://dev.mysql.com/downloads/connector/python
PyMySQL（纯python的mysql驱动）：https://pypi.python.org/pypi/PyMySQL （python3中使用，常用）
```

### 3.Django配置数据库
1、创建数据库
```
CREATE DATABASE IF NOT EXISTS testdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
2、配置文件settings里连接数据库,默认是sqllit3
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql’,#注意改成mysql后台
        'NAME': 'testdb',
        'USER':'root',
        'PASSWORD':'123456’,#就是连接mysql的密码
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}
```
3、如使用pymysql模块则在和项目project同名的__init__中
```
import pymysql
pymysql.install_as_MySQLdb()
```
4、创建model,继承自models.Model类
```
class UserInfo(models.Modle):
    name = models.CharField(max_length=50)
    pawd = models.CharField(max_length=32)

    def __str__(self)
        return self.name
```
5、数据库相关密令
```
python manage.py makemigrations
python manage.py migrate
python manage.py flush
```
注意：在开发过程中，数据库同步误操作之后，难免会遇到后面不能同步成功的情况，解决这个问题的一个简单粗暴方法是把migrations目录下的脚本（除__init__.py之外）全部删掉，再把数据库删掉之后创建一个新的数据库，数据库同步操作再重新做一遍。 

## 二、ORM关系对象映射
#### 1.ORM相关
用面向对象的方式去操作数据库的创建表以及增删改查等操作。其他语言中也有：
- PHP：activerecord
- Java：Hibernate 
- C#：Entity Framework

使用ROM优点： 
- 1.ORM使得我们的通用数据库交互变得简单易行，而且完全不用考虑该死的SQL语句。快速开发，由此而来。
- 2.可以避免一些新手程序猿写sql语句带来的性能问题。

使用ORM缺点:
- 1.性能有所牺牲，不过现在的各种ORM框架都在尝试各种方法，比如缓存，延迟加载登来减轻这个问题。效果很显著。
- 2.对于个别复杂查询，ORM仍然力不从心，为了解决这个问题，ORM一般也支持写raw sql。
- 3.通过QuerySet的query属性查询对应操作的sql语句

django中遵循 Code Frist 的原则，即：根据代码中定义的类来自动生成数据库表。

#### 2.ORM在Django如何表现
在models.py中创建类
```
from django.db import models
   
class userinfo(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()
```

#### 3.更多数据库字段
```
01、models.AutoField　　自增列 = int(11)
　　如果没有的话，默认会生成一个名称为 id 的列，如果要显示的自定义一个自增列，必须将给列设置为主键 primary_key=True。
02、models.CharField　　字符串字段
　　必须 max_length 参数
03、models.BooleanField　　布尔类型=tinyint(1)
　　不能为空，Blank=True
04、models.ComaSeparatedIntegerField　　用逗号分割的数字=varchar
　　继承CharField，所以必须 max_lenght 参数
05、models.DateField　　日期类型 date
　　对于参数，auto_now = True 则每次更新都会更新这个时间；auto_now_add 则只是第一次创建添加，之后的更新不再改变。
06、models.DateTimeField　　日期类型 datetime
　　同DateField的参数
07、models.Decimal　　十进制小数类型 = decimal
　　必须指定整数位max_digits和小数位decimal_places
08、models.EmailField　　字符串类型（正则表达式邮箱） =varchar
　　对字符串进行正则表达式
09、models.FloatField　　浮点类型 = double
10、models.IntegerField　　整形
11、models.BigIntegerField　　长整形
　　integer_field_ranges = {
　　　　'SmallIntegerField': (-32768, 32767),
　　　　'IntegerField': (-2147483648, 2147483647),
　　　　'BigIntegerField': (-9223372036854775808, 9223372036854775807),
　　　　'PositiveSmallIntegerField': (0, 32767),
　　　　'PositiveIntegerField': (0, 2147483647),
　　}
12、models.IPAddressField　　字符串类型（ip4正则表达式）,django1.10逐步废弃使用下面一种
13、models.GenericIPAddressField　　字符串类型（ip4和ip6是可选的）
　　参数protocol可以是：both、ipv4、ipv6
　　验证时，会根据设置报错
14、models.NullBooleanField　　允许为空的布尔类型
15、models.PositiveIntegerFiel　　正Integer
16、models.PositiveSmallIntegerField　　正smallInteger
17、models.SlugField　　减号、下划线、字母、数字
18、models.SmallIntegerField　　数字
　　数据库中的字段有：tinyint、smallint、int、bigint
19、models.TextField　　  字符串=longtext
20、models.TimeField　　  时间 HH:MM[:ss[.uuuuuu]]
21、models.URLField　　   字符串，地址正则表达式
22、models.BinaryField　　二进制
23、models.ImageField    图片,需要max_length
24、models.FilePathField 文件,需要max_length
```
#### 4.更多参数
```
01、null=True   # 数据库中字段是否可以为空
02、blank=True  # django的 Admin 中添加数据时是否可允许空值
03、primary_key = False    #主键，对AutoField设置主键后，就会代替原来的自增 id 列
04、auto_now、auto_now_add
　　auto_now      # 自动创建---无论添加或修改，都是当前操作的时间
　　auto_now_add  # 自动创建---永远是创建时的时间
05、choices
    GENDER_CHOICE = (
            (u'M', u'Male'),
            (u'F', u'Female'),
    )
    gender = models.CharField(max_length=2,choices = GENDER_CHOICE)

    gender_choice = (
        (0,'男'),
        (1,'女'),
    )
    gender = models.IntergetFiled(choice=gener_choice)  # 数据库中存储的是0，1但是显示的是男，女

06、max_length      # 在charfield必须指定最大长度
07、default　　      # 默认值
08、verbose_name　　 # Admin中字段的显示名称
09、name|db_column　 # 数据库中的字段名称
10、unique=True　　 # 不允许重复
11、db_index = True　　# 数据库索引
12、editable=True　　  # 在Admin里是否可编辑
13、error_messages=None　　# 在Admin错误提示
14、auto_created=False　　 # 自动创建
15、help_text　　   # 在Admin中提示帮助信息
16、validators=[]  # 自定义规则
17、upload-to      # 指定上传的路径
18、class Meta():
        verbose_name = '这张表的名字在admin后台的显示名字'
        verbose_name_plural = verbose_name
        ordering = ['-id']  # 根据id反向排序
```
