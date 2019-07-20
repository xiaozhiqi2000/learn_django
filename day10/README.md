# 今天主要内容
[django Model(三)实例操作]()

## 实例操作
### 1.查看mysite/blog/models.py
- 帐号UserProfile：一个帐号有用户名和密码。假设一个帐号对应是一个用户详情,在大多数情况下我们没 有必要将他们拆分成两张表，这里只是引出一对一的概念,（one－to－one）
- 用户详情表UserInfo：用户包括姓名,邮箱,地址,用户类型
- 用户组：这里组表现的是职位,有CEO,CTO,COO，一个用户可以有多个职位,一个职位也可以有多个用户,所以用户详情与用户组的关系就是多对多的关联关系（many－to－many）
- 主机：主机包括主机名和IP地址，假设一个用户组可以有多台主机,所以用户组与主机的关系是（one-to-many）

同步数据库
```
python manage.py makemigrations
python manage.py migrate
```
### 2.查看mysite/urls.py
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
### 3.查看mysite/blog/views.py
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
#### (3) 查看mysite/blog/views.py,单表,一对一,一对多,多对多操作
