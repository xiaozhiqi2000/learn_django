from django.shortcuts import render
from app01 import models
# Create your views here.
def addata(request):
    """
    批量添加数据
    :param request:
    :return:
    """
    # 批量插入Publisher表
    models.Publisher.objects.bulk_create([
        models.Publisher(name="人民出版社", address="福州", city="福州", state_province="福建", country="中国", website="http://www.pph166.com/"),
        models.Publisher(name="中国财经出版社", address="北京", city="北京", state_province="北京", country="中国", website="http://cfeph.cfemg.cn/"),
        models.Publisher(name="机械工业出版社", address="上海", city="上海", state_province="上海", country="中国", website="http://www.cmpedu.com/"),
        models.Publisher(name="新世纪出版社", address="深圳", city="深圳", state_province="广东", country="中国", website="http://www.gdpg.com.cn/"),
        models.Publisher(name="中国法制出版社", address="南昌", city="南昌", state_province="江西", country="中国", website="http://www.zgfzs.com/"),
        models.Publisher(name="人民邮电出版社", address="南宁", city="南宁", state_province="广西", country="中国", website="https://www.ptpress.com.cn/"),
        models.Publisher(name="中国农业出版社", address="北京", city="北京", state_province="北京", country="中国", website="http://www.ccap.com.cn/"),
        models.Publisher(name="人民卫生出版社", address="厦门", city="厦门", state_province="福建", country="中国", website="http://www.pmph.com/"),
        models.Publisher(name="石油工业出版社", address="广东", city="广东", state_province="广东", country="中国", website="http://www.petropub.com/"),
    ])

    # 批量插入Author表
    models.Author.objects.bulk_create([
        models.Author(name='ShiZhongyu'),
        models.Author(name='SunDasheng'),
        models.Author(name='LinDaiyu'),
        models.Author(name='LinChong'),
        models.Author(name='MaChao'),
        models.Author(name='XieYanke'),
        models.Author(name='TianBoguang'),
        models.Author(name='YuanChengzhi'),
    ])


    # 批量插入AuthorDetail表
    models.AuthorDetail.objects.bulk_create([
        models.AuthorDetail(sex=0, email="ShiZhongyu@qq.com", address="深圳市", birthday="1989-08-30", author_id=1,),
        models.AuthorDetail(sex=1, email="SunDasheng@qq.com", address="北京市", birthday="1988-01-30", author_id=2,),
        models.AuthorDetail(sex=0, email="LinDaiyu@qq.com", address="龙岩市", birthday="1985-05-30", author_id=3,),
        models.AuthorDetail(sex=1, email="LinChong@qq.com", address="广东市", birthday="1985-04-30", author_id=4,),
        models.AuthorDetail(sex=1, email="MaChao@qq.com", address="广西市", birthday="1986-02-28", author_id=5,),
        models.AuthorDetail(sex=0, email="XieYanke@qq.com", address="上海市", birthday="1987-08-30", author_id=6,),
        models.AuthorDetail(sex=1, email="TianBoguang@qq.com", address="南京市", birthday="1987-04-30", author_id=7,),
        models.AuthorDetail(sex=0, email="YuanChengzhi@qq.com", address="长沙市", birthday="1986-06-30", author_id=8,),
    ])

    # 批量插入Book表
    models.Book.objects.bulk_create([
        models.Book(title="鸟哥的Linux私房菜", publication_date="1984-06-30", price=36, publisher_id=1),
        models.Book(title="Linux内核设计与实现", publication_date="1983-05-30", price=60, publisher_id=2),
        models.Book(title="Linux入门到精通", publication_date="1981-04-30", price=45, publisher_id=1),
        models.Book(title="Python入门手册", publication_date="1989-08-30", price=64, publisher_id=3),
        models.Book(title="Python基础教程", publication_date="1985-06-30", price=37, publisher_id=4),
        models.Book(title="Python核心编程", publication_date="1982-04-30", price=52, publisher_id=3),
        models.Book(title="Go语言实战", publication_date="1987-01-30", price=49, publisher_id=5),
        models.Book(title="Go核心编程", publication_date="1983-09-30", price=20, publisher_id=6),
        models.Book(title="Go并发编程实战", publication_date="1987-06-30", price=30, publisher_id=5),
        models.Book(title="机器学习", publication_date="1983-08-30", price=50, publisher_id=7),
        models.Book(title="Linux就是这个范", publication_date="1984-02-18", price=26, publisher_id=8),
        models.Book(title="Php入门到精通", publication_date="1982-01-30", price=47, publisher_id=9),
    ])

    # 批量插入ManyToMang第三张表
    for i in range(1, 13):
        print(i)
        book_obj = models.Book.objects.get(id=i)
        import random
        num_list = []
        if len(num_list) == 2:
            num_list[0] = ""
            num_list[1] = ""
        num = random.randint(1, 8)
        num1 = random.randint(1, 8)
        num_list.append(num)
        if num == num1:
            num1 = random.randint(1, 8)
            num_list.append(num1)
        num_list.append(num1)
        book_obj.authors.add(*num_list)

    return render(request, 'addata.html')


def danbiao(request):
    """
    单表查询,Author是单表
    :param request:
    :return:
    """
    # all()是queryset对象 print(type(queryset))，就是类对象集合，所以要迭代取出值
    # queryset对象可以通过 print(queryset.query)得出查询语句

    queryset = models.Author.objects.all()
    for i in queryset:
        print(i.id, i.name)

    # filter是queryset对象，所以要迭代取出值，
    queryset1 = models.Author.objects.filter(id__gt=1, id__lt=5)
    for i in queryset1:
        print(i.id, i.name)

    # values也是queryset对象,需要迭代取值,values是字典
    queryset2 = models.Author.objects.filter(id__in=[1, 3, 5]).values('id', 'name')
    for i in queryset2:
        print(i['id'], i['name'])

    # values也是queryset对象,需要迭代取值,values是字典
    queryset3 = models.Author.objects.filter(id__range=[1, 6]).values('id', 'name')
    for i in queryset3:
        print(i['id'], i['name'])

    # values也是queryset对象,需要迭代取值,values是字典
    queryset4 = models.Author.objects.filter(name__contains="L").values('id', 'name')
    for i in queryset4:
        print(i['id'], i['name'])


    # values_list也是queryset对象,需要迭代取值,values_list返回的是一个元组,这种模板好像不好渲染
    queryset5 = models.Author.objects.filter(name='XieYanke').values_list('id', 'name')
    for i in queryset5:
        print(i[0], i[1])

    queryset6 = [1,2,3,4,5,6]

    # get是一个Author类 model 对象,不需要迭代取值,直接取,
    obj = models.Author.objects.get(id=3)
    print(type(obj))
    print(obj)  # 会自动执行UserInfo中__str__方法打印self.name所以是id=10的name
    print(obj.id, obj.name)

    return render(request, 'danbiao.html', locals())


def yiduiyi(request):
    """
    OneToOneField 一对一查询，Author与AuthorDetail是一个对一对应关系
    OneToOneField 约束在哪张表，从该表发起的查询称为正向查询
    :param request:
    :return:
    """
    # 正向查询，查询AuthorDetail所有用户信息，这种属于对象形式查找，
    queryset = models.AuthorDetail.objects.all()
    for i in queryset:
        print(i.sex, i.email, i.address, i.birthday, i.author.id, i.author.name)


    # 正向连表查询，连表操作通过OneToOneField对应的字段author通过双下划线__关联表的字段名字，这种双下划线属于条件查询
    queryset1 = models.AuthorDetail.objects.all().values('id', 'sex', 'email', 'address', 'birthday', 'author__name')
    for i in queryset1:
        print(i['id'], i['sex'], i['email'], i['address'], i['birthday'], i['author__name'])

    # first() 是取queryset的第一条，那么一条就是一个类对象，所以有first()的方法取出的不是一个queryset对象，是一个类对象
    # 相当于上面的 queryset1[0] 是一样的
    obj = models.AuthorDetail.objects.all().values('id', 'sex', 'email', 'address', 'birthday', 'author__name').first()
    print(obj['id'], obj['sex'], obj['email'], obj['address'], obj['birthday'], obj['author__name'])


    # 反向查询，通过Author表反查AuthorDetail表，这种属于对象式查找
    querysetf1 = models.Author.objects.all()
    for i in querysetf1:
        print(i.name, i.authordetail.email)


    # 反向查询，通过Author表反查AuthorDetail表，通过点.关联表点.关联表字段
    obj1 = models.Author.objects.filter(id=1).first()
    print(type(obj1))
    print(obj1.name, obj1.authordetail.sex, obj1.authordetail.email, obj1.authordetail.address, obj1.authordetail.birthday)


    # 反向连表查询
    obj2 = models.Author.objects.filter(id=1).values('name', 'authordetail__email', 'authordetail__address').first()
    print(type(obj2))
    print(obj2["name"], obj2["authordetail__email"], obj2["authordetail__address"])

    return render(request, 'yiduiyi.html', locals())


def yiduiduo(request):
    """
    一对多查询，Book和出版社publisher一对多关系
    一对多ForeignKey在多的那张表，从该表开始查询，称正向查询
    :param request:
    :return:
    """

    # all()取出是一个queryset对象所以需要循环迭代
    queryset = models.Book.objects.all()
    for i in queryset:
        print(i.id, i.title, i.publication_date, i.price, i.publisher, i.publisher.name, i.publisher.address)

    queryset2 = models.Book.objects.filter(title="Go语言实战")[0]
    print(queryset2.title, queryset2.publisher.name, queryset2.publisher.address)


    # 正向查询连表操作
    # values()是queryset对象但是后面firt()取第一条，返回字典
    # 连表的时候foreignkey对应字段名字__关联表字段
    obj = models.Book.objects.all().values('id', 'title', 'publication_date', 'price', "publisher__name").first()
    print(obj)
    print(obj['title'], obj['publication_date'], obj['price'], obj['publisher__name'])


    # obj2[0] 和上面 obj相同的，obj2是个queryset对象需要迭代取值
    obj2 = models.Book.objects.all().values('id', 'title', 'publication_date', 'price', "publisher__name", "authors__name")
    print(type(obj2))
    print(obj2)
    for i in obj2:
        print(i.keys())
        print(i.values())


    # 反向查询
    queryset3 = models.Publisher.objects.all()
    print(queryset3)
    print(type(queryset3))
    for i in queryset3:
        print(i.name)
        print(i.book_set.all())
        book_obj = i.book_set.all()
        for j in book_obj:
            print(j.title)
            print(j.price)




    # 反向查询连表操作
    obj4 = models.Publisher.objects.all().values('name', 'book__title', 'book__price').first()
    print(obj4['name'], obj4['book__title'], obj4['book__price'])

    queryset5 = models.Publisher.objects.all().values('name', 'book__title', 'book__price')
    print(queryset5.query)
    for i in queryset5:
        print(i['name'])
        print(i['book__title'])
        print(i['book__price'])

    return render(request, 'yiduiduo.html', locals())


def duoduiduo(request):
    """
    ManyToManyField
    :param request:
    :return:
    """
    # 在关联连表的时候不知道填什么字段，故意填错，django会提示可以填入的字段

    # 正向添加数据,多对多的第三表存储的是两张表的主键id
    book_obj = models.Book.objects.get(id=1)
    author_obj = models.Author.objects.get(id=1)
    author_objs = models.Author.objects.all()

    book_obj.authors.add(author_obj)
    book_obj.authors.add(*author_objs)
    book_obj.authors.add(1)
    book_obj.authors.add(*[1, 2, 4])

    # 正向删除数据
    book_obj.authors.clear()   # 清空所有与第三张表usergroup id=1的所有数据
    book_obj.authors.remove(*[2, 3, 4])  # 删除，2,3,4条数据

    # 正向查询数据
    book_obj1 = models.Book.objects.get(id=1)
    queryset1 = book_obj1.authors.all()
    for i in queryset1:
        print(i.id)
        print(i.name)
        print(i.email)
        print(i.address)
        print(i.get)

    # 正向关联表查询
    queryset2 = models.Book.objects.all().values('id', 'title', 'price', 'authors__name', 'publisher__name')
    print(queryset2.query)
    for i in queryset2:
        print(i['id'], i['title'], i['price'], i['authors__name'], i['publisher__name'])


    # 反向添加数据
    user_info_obj = models.UserInfo.objects.get(id=1)
    group_obj1 = models.UserGroup.objects.get(id=1)
    group_obj2 = models.UserGroup.objects.all()
    obj2 = user_info_obj.usergroup_set.add(group_obj1)
    obj3 = user_info_obj.usergroup_set.add(*group_obj2)
    user_info_obj.usergroup_set.add(1)
    user_info_obj.usergroup_set.add(*[1,2,3,4])

    # 反向删除数据
    user_info_obj.usergroup_set.clear() # 清空所有第三张表userinfo id=1的所有数据
    user_info_obj.usergroup_set.remove(*[2,3,4])

    # 反向查询
    user_info_obj = models.UserInfo.objects.get(id=1)
    obj4 = user_info_obj.usergroup_set.all()
    print(obj4)
    print(type(obj4))
    for i in obj4:
        print(i.id)
        print(i.caption)

    # 反向连表查询
    dic1 = models.UserInfo.objects.all().values('name','email','address','usergroup__caption')
    print(dic1)

    return render(request,'duoduiduo.html',locals())