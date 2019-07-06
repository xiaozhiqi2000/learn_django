# 今天主要内容
[django Settings配置文件]()

参考：

[Django1.11 官网settings](https://docs.djangoproject.com/en/1.11/ref/settings/)

[Django1.11 官网settings](https://docs.djangoproject.com/en/1.11/topics/settings/)

### 1.django默认创建app会在这里注册,在创建app时,需要手动添加来
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]
```
### 2.数据库配置,默认是sqlite3,如使用MYSQL
```
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME':'dbname',
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': '',
    'PORT': '',
    }
}
```
由于Django内部连接MySQL时使用的是MySQLdb模块，而python3中还无此模块，所以需要使用pymysql来代替
如下设置放置的与project同名的配置的 __init__.py文件中
```
import pymysql
pymysql.install_as_MySQLdb()
```

### 3.templates是用于放置模板html,在django1.9以上中会自动创建并设置,之前版本要自己添加
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
``` 

### 4.static静态文件配置
- static是自己创建的目录用于放置css,js,image，需要在settings中设置这个目录
```
# STATIC_URL = '/static/' 这个路径是对应<script src="/static/jquery-2.2.4.min.js"></script> 中 src="/static/ 这个是别名
# 如果改为 STATIC_URL = '/abc/' 那么前端 js 引用则改为 <script src="/abc/jquery-2.2.4.min.js"></script>
# 这样后端路径不管怎么变，前端依然引用的是个别名

STATIC_URL = '/static/'  
 
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

### 5.upload上传目录设置
- upload是自己创建的目录用于图片上传，需要settings中设置 MEDIA_URL
#### settings怎么设置呢？
```
MEDIA_URL = '/upload/'       #MEDIA_ROOT是本地路径的绝对路径，一般是这样写
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')  #MEDIA_URL：是指从浏览器访问时的地址前缀,这里也是一个别名
```
#### url怎么设置呢？
```
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^uploadimg/', views.uploadImg),
    url(r'^showimg/', views.uploadImg),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

# 以前的django版本是这样的
# url(r'^upload/(?P<path>.*)$', "django.views.static.serve", {"document_root": settings.MEDIA_ROOT,}), 
```
#### models怎么设置呢？
```
from django.db import models

class IMG(models.Model):
    '''
    图片上传的路径就会在/upload/2019/07/06/a1.jpg
    浏览器访问：http://127.0.0.1:8000/upload/2019/07/06/a1.jpg
    '''
    head_img = models.ImageField(max_length=200,upload_to='%Y/%m/%d',\
                                default='default.png',null=True,blank=True)
```
#### views怎么设置？
```
from django.shortcuts import render
from django.db import models

def uploadImg(request):
    if request.method == 'POST':
        new_img = models.IMG(
            head_img=request.FILES.get('img')
        )
        new_img.save()
    return render(request, 'uploadimg.html')

def showImg(request):
    imgs = models.IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    return render(request, 'showimg.html', content)
```
#### html怎么设置？
uploadimg.html
```
<form action="/uploadimg/" method="POST" enctype="multipart/form-data">
    <input type="file" name="img">
    <button type="submit">上传</button>
    {% csrf_token %}
</form>
```
showimg.html
```
{% for img in imgs %}
    <img src='{{ img.img.url }}' />
{% endfor %}
```

### 6.文件上传
参考：

[Django1.11 官网settings](https://docs.djangoproject.com/en/1.11/topics/settings/)

文件上传类似,前端form属性要有enctype='multipart/form-data'，models中的字段为models.FileField(max_length='',upload_to='')

#### url 设置
```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^uploadfile/', views.upload_file),
]
```
#### views 设置
```
from django.shortcuts import render,redirect

def upload_file(request):
    if request.method == 'POST':
        for item in request.FILES:
            obj = request.FILES.get(item,None)
            filename = obj.name
            path = 'upload/file' + filename
            with open(path, 'wb+') as f:
                for chunk in obj.chunks():
                    f.write(chunk)

            return redirect('/uploadfile/')

    return render(request, 'uploadfile.html')
```
#### html
```
<form action="/uploadfile/" method="POST" enctype="multipart/form-data">
    <input type="file" name="img">
    <button type="submit">上传</button>
    {% csrf_token %}
</form>
```












