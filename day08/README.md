# 今天主要内容
[django Model(二)]()

## 一、QuerySet API
参考：

[Django1.11 官网具有QuerySet的方法](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#methods-that-return-new-querysets)

[Django1.11 官网不具有QuerySet的方法](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#methods-that-do-not-return-querysets)

### 1.QuerySet 特点
- QuerySet 是一个对象集合,所以取值是要通过迭代取值的,也可以切片
- QuerySet 不会马上执行sql，而是当调用QuerySet的时候才执行

### 2.QuerySet 惰性机制
#### (1)Django的queryset是惰性的
```
Django的queryset对应于数据库的若干记录（row），通过可选的查询来过滤。例如，下面的代码会得
到数据库中名字为‘Dave’的所有的人:person_set = Person.objects.filter(first_name="Dave")
上面的代码并没有运行任何的数据库查询。你可以使用person_set，给它加上一些过滤条件，或者将它传给某个函数，
这些操作都不会发送给数据库。这是对的，因为数据库查询是显著影响web应用性能的因素之一。
```
#### (2)要真正从数据库获得数据，你可以遍历queryset或者使用if queryset,总之你用到数据时就会执行sql.
```
为了验证这些,需要在settings里加入 LOGGING(验证方式)
obj=models.Book.objects.filter(id=3)
# for i in obj:
#     print(i)

# if obj:
#     print("ok")
```
#### (3)queryset是具有cache的
```
当你遍历queryset时，所有匹配的记录会从数据库获取，然后转换成Django的model。这被称为执行
（evaluation）.这些model会保存在queryset内置的cache中，这样如果你再次遍历这个queryset，
你不需要重复运行通用的查询。
obj=models.Book.objects.filter(id=3)

# for i in obj:
#     print(i)

## models.Book.objects.filter(id=3).update(title="GO")
## obj_new=models.Book.objects.filter(id=3)

# for i in obj:
#     print(i)   #LOGGING只会打印一次
```
#### (4)简单的使用if语句进行判断也会完全执行整个queryset并且把数据放入cache，虽然你并不需要这些数据！为了避免这个，可以用exists()方法来检查是否有数据：
```
obj = Book.objects.filter(id=4)
#  exists()的检查可以避免数据放入queryset的cache。
if obj.exists():
    print("hello world!")
```
#### (5)当queryset非常巨大时，cache会成为问题
```
处理成千上万的记录时，将它们一次装入内存是很浪费的。更糟糕的是，巨大的queryset可能会锁住系统
进程，让你的程序濒临崩溃。要避免在遍历数据的同时产生queryset cache，可以使用iterator()方法
来获取数据，处理完数据就将其丢弃。
objs = Book.objects.all().iterator()

# iterator()可以一次只从数据库获取少量数据，这样可以节省内存
for obj in objs:
    print(obj.name)

#BUT,再次遍历没有打印,因为迭代器已经在上一次遍历(next)到最后一次了,没得遍历了
for obj in objs:
    print(obj.name)

#当然，使用iterator()方法来防止生成cache，意味着遍历同一个queryset时会重复执行查询。所以使
#用iterator()的时候要当心，确保你的代码在操作一个大的queryset时没有重复执行查询
```
总结:
    queryset的cache是用于减少程序对数据库的查询，在通常的使用下会保证只有在需要的时候才会查询数据库。
使用exists()和iterator()方法可以优化程序对内存的使用。不过，由于它们并不会生成queryset cache，可能
会造成额外的数据库查询。

## 二、操作数据库
#### 1.增加创建数据 create()、bulk_createa()
```
# create 第一种方式
models.类名.objects.create(hostname="name") 
 
# create 第二种方式，推荐这种
models.类名.objects.create(**{"hostname":"name"})
  
# save 第三种方式
obj = models.类名(hostname="name")
obj.save()
   
# save 第四种方式，其实和第三种是一样的，推荐第二种
obj = models.类名()
obj.hostname = "name"
obj.save()
    
     
# bulk_create() 批量创建数据
models.类名.objexts.bulk_create([
    models.类名("hostname"="name", "password"="123"),
    models.类名("hostname"="name1", "password"="1234"),
])

注意：使用第二种方式即可,批量使用bulk_create()即可
```
#### 2.更新数据 update()
```
# 第一种方式，推荐这种,而且高效
models.类名.objects.filter(id=2).update(hostname='tomcat') 
 
# 第二种方式
obj = models.类名.objects.get(id=2)
obj.hostname = 'tomcat'
obj.save()

注意：第二种方式修改不能用get的原因是：update是QuerySet对象的方法，get返回的是一个model对象，它没有update方法，而filter返回的是一个QuerySet对象(filter里面的条件可能有多个条件符合，比如name＝'alvin',可能有两个name＝'alvin'的行数据)
```
#### 3.删除数据 delete()
```
models.类名.objects.get(id=2).delete()      # 不建议
models.类名.objects.filter(id=2).delete()   # 推荐使用
models.类名.objects.all().delete()
```
#### 4.查询数据 get()、filter()、all()
```
models.类名.objects.get(id=123)           # 获取单条数据，不存在则报错，多条数据也报错（不建议），
models.类名.objects.all()                 # 获取全部，是一个Queryset对象需要迭代取值
models.类名.objects.filter(name='tomcat') # 获取指定条件的数据，是一个Queryset对象需要迭代取值
```
#### 5.显示字段 values()、values_list()
```
models.类名.objects.get(id=123).values('id','name')  # 返回的是queryset字典
models.类名.objects.get(id=123).values__list('id','name') # 返回的是queryset元组
```
#### 6.数量 count()
```
models.类名.objects.filter(name='tomcat').count()
models.类名.objects.get(name='tomcat').count()
models.类名.objects.all().count()
```
#### 7.去重 distinct()
```
models.类名.objects.values('字段').distinct()
```
#### 8.大于小于：__gt,__lt,__gte,__lte
```
models.类名.objects.filter(id__gt=1)              # 获取id大于1的值
models.类名.objects.filter(id__lt=10)             # 获取id小于10的值
models.类名.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值
```
#### 9.等于多个值：__in
```
models.类名.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
models.类名.objects.exclude(id__in=[11, 22, 33])  # not in
```
#### 10.模糊查询：__contains,__icontains　　
```
models.类名.objects.filter(name__contains="ven")
models.类名.objects.filter(name__icontains="ven")    # icontains大小写不敏感
models.类名.objects.exclude(name__icontains="ven")
```
#### 11.范围查询：__range 其他类似：__startswith,__endswith, __iendswith, __istartswith　　
```
models.类名.objects.filter(id__range=[1, 2])   # 范围bettwen and
```
#### 12.exists() 
如果QuerySet包含数据，就返回True，否则返回False
```
queryset = models.类名.objects.fiter(id=2)
if queryset.exists():
    print("True")
```
#### 13.排序：order_by("name") 相当于asc；order_by("-name") 相当于desc；　　
```
models.类名.objects.filter(name='seven').order_by('id')     # asc,从小到大
models.类名.objects.filter(name='seven').order_by('-id')   # desc,从大到小
```
#### 14.返回第n-m条：第n条[0]；前两条[0:2] limit 、offset
``` 
models.类名.objects.all()[10:20]
```
#### 15.分组与聚合：group_by,annotate,aggregate
[Django1.11 官网aggregation](https://docs.djangoproject.com/en/1.11/topics/db/aggregation/)

[Django1.11 官网annotate](https://docs.djangoproject.com/en/1.11/topics/db/annotate/)
```
annotate(*args, **kwargs)：可以为 QuerySet 中的每个对象添加注解。可以通过计算查询结果中每个对象所关联的对象集合，从而得出总计值(也可以是平均值或总和，等等)
aggregate(*args, **kwargs)：通过对 QuerySet 进行计算，返回一个聚合值的字典。 aggregate() 中每个参数都指定一个包含在字典中的返回值。用于聚合查询
Avg(返回所给字段的平均值)
Count(根据所给的关联字段返回被关联 model 的数量)
Max(返回所给字段的最大值)
Min(返回所给字段的最小值)
Sum(计算所给字段值的总和)

# group by
from django.db.models import Count, Min, Max, Sum
# models.类名.objects.filter(c1=1).values('id').annotate(c=Count('num'))
# SELECT "app01_类名"."id", COUNT("app01_类名"."num") AS "c" FROM "app01_类名" WHERE "app01_类名"."c1" = 1 GROUP BY "app01_类名"."id"i
```

## 三、原生SQL
注意：使用原生sql的方式主要目的是解决一些很复杂的sql，不能用ORM的方式写出的问题。
- extra：结果集修改器 - 一种提供额外查询参数的机制
- raw：执行原始sql并返回模型实例，最适合用于查询,(异常：Raw query must include the primary key,返回结果必须包含主键)
- 直接执行自定义SQL（这种方式完全不依赖model，前面两种方式还是要依赖于model），适合增删改

```
A.使用extra：
>>> Book.objects.filter(publisher__name='广东人民出版社').extra(where=['price>50’])
>>> Book.objects.filter(publisher__name='广东人民出版社', price__gt=50)
>>> Book.objects.extra(select={'count':'select count(*) from hello_book'})

B.使用raw：
>>> Book.objects.raw('select * from hello_book')

C.自定义sql：
from django.db import connection
cursor = connection.cursor()            #获得一个游标(cursor)对象
 
cursor.execute("insert into hello_author(name) values('郭敬明')")    #插入操作
cursor.execute("update hello_author set name = '韩寒' where name='郭敬明'")  #更新操作 
cursor.execute("delete from hello_author where name='韩寒'")   #删除操作
cursor.execute('select * from hello_author')  #查询操作
raw = cursor.fetchone()                       #返回结果行
cursor.fetchall()

```
[Django1.11 官网原生sql](https://docs.djangoproject.com/en/1.11/topics/db/sql/)

## 四、自定义Manager
https://docs.djangoproject.com/en/1.11/topics/db/managers/
