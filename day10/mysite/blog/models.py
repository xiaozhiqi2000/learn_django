# encoding:utf8
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user_info = models.OneToOneField('UserInfo')

    def __str__(self):       # __unicode__ on python2
        return self.username


class UserInfo(models.Model):
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

    caption = models.CharField(max_length=64)

    user_info = models.ManyToManyField('UserInfo')

    def __str__(self):       # __unicode__ on python2
        return self.caption


class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()
    user_group = models.ForeignKey('UserGroup')

    def __str__(self):       # __unicode__ on python2
        return self.hostname