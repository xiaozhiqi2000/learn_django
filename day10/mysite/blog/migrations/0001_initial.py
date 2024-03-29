# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-06 05:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='IMG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_img', models.ImageField(blank=True, default='article/default.png', max_length=200, null=True, upload_to='article/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=128)),
                ('user_type', models.IntegerField(choices=[(0, '普通用户'), (1, '高级用户')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('user_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='usergroup',
            name='user_info',
            field=models.ManyToManyField(to='blog.UserInfo'),
        ),
        migrations.AddField(
            model_name='host',
            name='user_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserGroup'),
        ),
    ]
