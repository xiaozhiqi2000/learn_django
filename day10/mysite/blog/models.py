# encoding:utf8
from django.db import models

class IMG(models.Model):
    '''
    图片上传的路径就会在/upload/article/2016/09/23/a1.jpg
    浏览器访问：http://127.0.0.1:8000/upload/article/2016/09/23/a1.jpg
    '''
    head_img = models.ImageField(max_length=200, upload_to='article/%Y/%m/%d', \
                                default='article/default.png', null=True, blank=True)

# Create your models here.
class UserProfile(models.Model):
    """
    账户表，一个帐号对应一个用户的用户信息，所以用 OneToOneField
    """
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user_info = models.OneToOneField('UserInfo')

    def __str__(self):       # __unicode__ on python2
        return self.username


class UserInfo(models.Model):
    """
    用户信息表
    """
    user_type_choice = (
        (0, '普通用户'),
        (1, '高级用户'),
    )
    user_type = models.IntegerField(choices=user_type_choice)
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    address = models.CharField(max_length=128)


    def __str__(self):       # __unicode__ on python2
        return self.name


class UserGroup(models.Model):
    """
    用户组表，一个组对应多个用户，一个用户可以有多个用户组，所以用 ManyToManyField
    """
    caption = models.CharField(max_length=64)

    user_info = models.ManyToManyField('UserInfo')

    def __str__(self):       # __unicode__ on python2
        return self.caption


class Host(models.Model):
    """
    主机表，一个用户组对应多个主机，这里假设一个主机不能对用多个用户组，所以用 ForeignKey
    """
    hostname = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()
    user_group = models.ForeignKey('UserGroup')

    def __str__(self):       # __unicode__ on python2
        return self.hostname