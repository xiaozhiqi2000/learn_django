# encoding:utf8
from django.shortcuts import render,redirect
from blog import models

def addata(request):
    """
    批量添加数据
    :param request:
    :return:
    """
    # 批量插入UserInfo表
    models.UserInfo.objects.bulk_create([
        models.UserInfo(user_type=0, name='ShiZhongyu', email='shizhongyu@163.com', address='深圳市'),
        models.UserInfo(user_type=0, name='SunDasheng', email='sundasheng@163.com', address='佛山市'),
        models.UserInfo(user_type=0, name='LinDaiyu', email='lindaiyu@163.com', address='揭阳市'),
        models.UserInfo(user_type=0, name='LinChong', email='linchong@163.com', address='中山市'),
        models.UserInfo(user_type=0, name='MaChao', email='machao@126.com', address='福州市'),
        models.UserInfo(user_type=0, name='XieYanke', email='xieyanke@126.com', address='厦门市'),
        models.UserInfo(user_type=1, name='Xiaoiao', email='xiaoqiao@yahoo.com', address='漳州市'),
        models.UserInfo(user_type=1, name='TianBoguang', email='tianboguang@qq.com', address='龙岩市'),
        models.UserInfo(user_type=1, name='YuanChengzhi', email='yuanchengzhi@qq.com', address='北京市'),
        models.UserInfo(user_type=0, name='RenYingying', email='renyingying@360.com', address='上海市'),
        models.UserInfo(user_type=0, name='DiaoChan', email='diaochan@baidu.com', address='南京市'),
        models.UserInfo(user_type=0, name='LuWushuang', email='luwushuang@ali.com', address='青岛市'),
        models.UserInfo(user_type=0, name='XueBaochai', email='xuebaochai@live.com', address='浙江市'),
        models.UserInfo(user_type=1, name='XiaoDasheng', email='xiaodasheng@gmail.com', address='伊拉克'),
        models.UserInfo(user_type=1, name='SunWuKong', email='sunwukong@gmail.com', address='美国市'),
        models.UserInfo(user_type=1, name='ZhuBaJie', email='zhubajie@gmail.com', address='广东市'),
    ])

    # 批量插入UserProfile表
    userprofile_list = []
    for i in range(1, 17):
        username = 'zhanghao' + str(i)
        password = '123456'
        userinfo = i
        uprofile = models.UserProfile(username=username, password=password, user_info_id=userinfo)
        userprofile_list.append(uprofile)
    models.UserProfile.objects.bulk_create(userprofile_list)

    # 批量插入UserGroup表
    models.UserGroup.objects.bulk_create([
        models.UserGroup(caption='CTO'),
        models.UserGroup(caption='CEO'),
        models.UserGroup(caption='COO'),
    ])


    # 批量插入Host表
    models.Host.objects.bulk_create([
        models.Host(hostname='c1.salt.com', ip='192.168.1.1', user_group_id=1),
        models.Host(hostname='c2.salt.com', ip='192.168.1.2', user_group_id=1),
        models.Host(hostname='c3.salt.com', ip='192.168.1.3', user_group_id=1),
        models.Host(hostname='c4.salt.com', ip='192.168.1.4', user_group_id=1),
        models.Host(hostname='c5.salt.com', ip='192.168.1.5', user_group_id=1),
        models.Host(hostname='c6.salt.com', ip='192.168.1.6', user_group_id=2),
        models.Host(hostname='c7.salt.com', ip='192.168.1.7', user_group_id=2),
        models.Host(hostname='c8.salt.com', ip='192.168.1.8', user_group_id=2),
        models.Host(hostname='c9.salt.com', ip='192.168.1.9', user_group_id=2),
        models.Host(hostname='c10.salt.com', ip='192.168.1.10', user_group_id=2),
        models.Host(hostname='c11.salt.com', ip='192.168.1.11', user_group_id=3),
        models.Host(hostname='c12.salt.com', ip='192.168.1.12', user_group_id=3),
        models.Host(hostname='c13.salt.com', ip='192.168.1.13', user_group_id=3),
        models.Host(hostname='c14.salt.com', ip='192.168.1.14', user_group_id=3),
        models.Host(hostname='c15.salt.com', ip='192.168.1.15', user_group_id=3),
    ])

    return render(request, 'addata.html')


def danbiao(request):
    """
    单表查询
    :param request:
    :return:
    """
    # filter是querset对象，所以要迭代取出值
    queryset = models.UserInfo.objects.filter(name='ShiZhongyu')
    """
    print(queryset.query)
    print(type(queryset))
    for item in queryset:
        print(item.id)
        print(item.user_type)
        print(item.name)
        print(item.email)
        print(item.address)
    """


    # get是userinfo类 model 对象,不需要迭代取值,直接取,
    obj = models.UserInfo.objects.get(id=10)
    """
    print(type(obj))
    print(obj)  会自动执行UserInfo中__str__方法打印self.name所以是id=10的name
    print(obj.id)
    print(obj.name)
    print(obj.user_type)
    print(obj.email)
    print(obj.address)
    """
    id=obj.id
    name=obj.name
    user_type=obj.user_type
    email=obj.email
    address=obj.address

    # values也是queryset对象,需要迭代取值,values是字典
    obj1 = models.UserInfo.objects.filter(name='DiaoChan').values('id', 'name')
    """
    print(type(obj1))
    for i in obj1:
        print(i['id'])
        print(i['name'])
    """

    # values_list也是queryset对象,需要迭代取值,values_list返回的是一个元组,这种模板好像不好渲染
    obj2 = models.UserInfo.objects.filter(name='XieYanke').values_list('id', 'name')
    """
    print(type(obj2))
    for i in obj2:
        print(i[0])
        print(i[1])
    """

    # all() 也是个queryset对象，也是个字典集合
    obj3 = models.UserInfo.objects.all()
    """
    print(type(obj3))
    for iter in obj3:
        print(iter.id)
        print(iter.name)
    """

    return render(request, 'danbiao.html', locals())


def yiduiyi(request):
    """
    OneToOneField 一对一查询
    :param request:
    :return:
    """
    # 正向查询
    u_profile = models.UserProfile.objects.all()
    """
    for i in u_profile:
        print(i.id)
        print(i.username)
        print(i.password)
        print(i.user_info.get_user_type_display())
        print(i.user_info.name)
        print(i.user_info.email)
        print(i.user_info.address)
    """

    # 正向连表查询
    u_profile1 = models.UserProfile.objects.values('username', 'password', 'user_info__user_type', 'user_info__name')
    for i in u_profile1:
        print(i['username'])

    obj = models.UserProfile.objects.values('username', 'password', 'user_info__user_type', 'user_info__name').first()
    print(obj['username'])
    print(obj['password'])
    print(obj['user_info__user_type'])
    print(obj['user_info__name'])

    # 反向查询userprofile表
    user_info_obj = models.UserInfo.objects.filter(id=1).first()
    print(type(user_info_obj))
    print(user_info_obj.user_type)
    print(user_info_obj.get_user_type_display())
    print(user_info_obj.userprofile.password)

    # 反向连表查询
    user_info_obj1 = models.UserInfo.objects.filter(id=1).values('email', 'userprofile__username').first()
    print(type(user_info_obj1))
    print(user_info_obj1.keys())
    print(user_info_obj1.values())

    return render(request, 'yiduiyi.html', locals())


def yiduiduo(request):
    """
    一对多查询
    :param request:
    :return:
    """
    # 一对多ForeignKey在多的那张表，从该表开始查询，称正向查询
    # all()取出是一个queryset对象所以需要循环迭代
    obj = models.Host.objects.all()
    """
    for i in obj:
        print(i.id)
        print(i.hostname)
        print(i.ip)
        print(i.user_group.caption)
    """

    # 正向查询连表操作
    # values()是queryset对象但是后面firt()取第一条，返回字典
    # 连表的时候foreignkey对应字段名字__关联表字段
    obj1 = models.Host.objects.all().values('id', 'hostname', 'ip', 'user_group__caption').first()
    """
    print(obj1)
    print(obj1['hostname'])
    print(obj1['user_group__caption'])
    """

    # obj2[0] 和上面 obj1相同的，obj2是个queryset对象需要迭代取值
    obj2 = models.Host.objects.all().values('id', 'hostname', 'ip',  'user_group__caption')
    """
    print(type(obj2))
    for i in obj2:
        print(i.keys())
        print(i.values())
    """

    # 反向查询
    obj3 = models.UserGroup.objects.all()
    print(obj3)
    print(type(obj3))
    for i in obj3:
        print(i.caption)
        print(i.host_set.all())
        host_obj = i.host_set.all()
        for j in host_obj:
            print(j.hostname)
            print(j.ip)

    # 反向查询连表操作
    obj4 = models.UserGroup.objects.all().values('caption', 'host__hostname').first()
    print(obj4['caption'])
    print(obj4['host__hostname'])

    obj5 = models.UserGroup.objects.all().values('caption', 'host__hostname')
    for i in obj5:
        print(i['caption'])
        print(i['host__hostname'])

    # 一对多,三表关联
    allobj = models.Host.objects.filter(user_group__user_info__user_type=0)
    print(allobj.query)
    print(type(allobj))
    for i in allobj:
        print(i)
        print(i.user_group.caption)

    return render(request, 'yiduiduo.html', locals())


def duoduiduo(request):
    """
    ManyToManyField
    :param request:
    :return:
    """
    # 在关联连表的时候不知道填什么字段，故意填错，django会提示可以填入的字段

    # 正向添加数据,多对多的第三表存储的是两张表的主键id
    group_obj = models.UserGroup.objects.get(id=1)
    user_info_obj = models.UserInfo.objects.get(id=1)
    user_info_objs = models.UserInfo.objects.all()


    group_obj.user_info.add(user_info_obj)
    group_obj.user_info.add(*user_info_objs)
    group_obj.user_info.add(1)
    group_obj.user_info.add(*[1, 2, 4])

    # 正向删除数据
    group_obj.user_info.clear()   # 清空所有与第三张表usergroup id=1的所有数据
    group_obj.user_info.remove(*[2, 3, 4])  # 删除，2,3,4条数据

    # 正向查询数据
    group_obj = models.UserGroup.objects.get(id=1)
    obj = group_obj.user_info.all()
    for i in obj:
        print(i.id)
        print(i.name)
        print(i.email)
        print(i.address)
        print(i.get_user_type_display())

    # 正向关联表查询
    dic = models.UserGroup.objects.all().values('caption','user_info__name','user_info__address','user_info__email')
    print(dic)


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
    print(dic)

    return render(request,'duoduiduo.html',locals())

