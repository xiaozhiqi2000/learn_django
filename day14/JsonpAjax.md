# 今天主要内容
[JsonP Ajax]()

## 一、JSONP JS实现跨域

JSONP是JSON with Padding的简称，从不同的域名那获取资料，即跨域读取数据，实则是浏览器不允许不同域名之间访问，但是带src属性标签则可以跨域
- img
- iframe
- script

JSONP就像是JSON+Padding一样(Padding这里理解为填充),利用script标签的src属性，通过javascript callback的形式实现跨域访问

举个例子,服务器1向服务器2请求数据
```
### 服务器1 http://127.0.0.1:8001/login

def login(request):
   print('hello ajax')
   return render(request,'index.html')

### 返回用户的index.html
<h1>发送JSONP数据</h1>

<script>
    function fun1(arg){
        alert("hello"+arg)
    }
</script>
<script src="http://127.0.0.1:8002/get_byjsonp/"></script>  //返回：<script>fun1("python")</script>

### 服务器2 http://127.0.0.1:8002/get_byjsonp

def get_byjsonp(req):
    print('8002...')
    return HttpResponse('fun1("python")')
```
这其实就是JSONP的简单实现模式，或者说是JSONP的原型：创建一个回调函数，然后在远程服务上调用这个函数并且将JSON 数据形式作为参数传递，完成回调。

将JSON数据填充进回调函数，这应该就是JSONP的JSON+Padding的含义。

一般情况下，这个script标签能够动态的调用，而不是像上面因为固定在html里面所以没等页面显示就执行了，很不灵活。可以通过javascript动态的创建script标签，就可以灵活调用远程服务了。
```
<button onclick="f()">submit</button>

<script>
    function addScriptTag(src){
     var script = document.createElement('script');
         script.setAttribute("type","text/javascript");
         script.src = src;
         document.body.appendChild(script);
         document.body.removeChild(script);
    }
    function fun1(arg){
        alert("hello"+arg)
    }
    
    function f(){
         addScriptTag("http://127.0.0.1:8002/get_byjsonp/")
    }
</script>
```
为了更加灵活，现在将你自己在客户端定义的回调函数的函数名传送给服务端，服务端则会返回以你定义的回调函数名的方法，将获取的json数据传入这个方法完成回调：
```
<button onclick="f()">submit</button>

<script>
    function addScriptTag(src){
     var script = document.createElement('script');
         script.setAttribute("type","text/javascript");
         script.src = src;
         document.body.appendChild(script);
         document.body.removeChild(script);
    }
    function SayHi(arg){
        alert("Hello "+arg)
    }

    function f(){
         addScriptTag("http://127.0.0.1:8002/get_byjsonp/?callbacks=SayHi")
    }
</script>


----------------------views.py
def get_byjsonp(req):

    func=req.GET.get("callbacks")

    return HttpResponse("%s('python')"%func)
```

## 二、JSONP JQuery Ajax实现跨域
jQuery框架也当然支持JSONP，可以使用$.getJSON(url,[data],[callback])方法
```
<script type="text/javascript">
    $.getJSON("http://127.0.0.1:8002/get_byjsonp?callback=?",function(arg){
        alert("hello"+arg)
    });
</script>
```
结果是一样的，要注意的是在url的后面必须添加一个callback参数，这样getJSON方法才会知道是用JSONP方式去访问服务，callback后面的那个问号是内部自动生成的一个回调函数名。

此外，如果说我们想指定自己的回调函数名，或者说服务上规定了固定回调函数名该怎么办呢？我们可以使用$.ajax方法来实现
```
<script type="text/javascript" src="/static/jquery-2.2.3.js"></script>

<script type="text/javascript">
   $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",
        jsonp: 'callbacks',
        jsonpCallback:"SayHi"
   });
    function SayHi(arg){
        alert(arg);
    }
</script>
 
#--------------------------------- http://127.0.0.1:8002/get_byjsonp
 def get_byjsonp(req):

    callback=req.GET.get('callbacks')
    print(callback)
    return HttpResponse('%s("python")'%callback)
```
当然，最简单的形式还是通过回调函数来处理
```
<script type="text/javascript" src="/static/jquery-2.2.3.js"></script>

<script type="text/javascript">
   $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",            //必须有，告诉server，这次访问要的是一个jsonp的结果。
        jsonp: 'callbacks',          //jQuery帮助随机生成的：callbacks="wner"
        success:function(data){
            alert(data)
        }
   });

</script>
 #-------------------------------------http://127.0.0.1:8002/get_byjsonp
def get_byjsonp(req):

    callbacks=req.GET.get('callbacks')
    print(callbacks)                 #wner  

return HttpResponse("%s('python')"%callbacks)
```
jsonp: 'callbacks'就是定义一个存放回调函数的键，jsonpCallback是前端定义好的回调函数方法名'SayHi'，server端接受callback键对应值后就可以在其中填充数据打包返回了; 

jsonpCallback参数可以不定义，jquery会自动定义一个随机名发过去，那前端就得用回调函数来处理对应数据了。

利用jQuery可以很方便的实现JSONP来进行跨域访问。

**JSONP一定是GET请求**
```
<button onclick="f()">submit</button>

<script src="/static/jquery-1.8.2.min.js"></script>
<script type="text/javascript">
    function f(){
        $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",
        jsonp: 'callbacks',
        success :function(data){        //传过来的数据会被转换成js对象
            console.log(data);          //Object {name: Array[2]}
            console.log(typeof data);   //object
            console.log(data.name)      //["alex", "alvin"]
        }
   });
    }
</script>
---------------------------------------------views.py
def get_byjsonp(req):

    func=req.GET.get("callbacks")

    a=json.dumps({'name':('alex','alvin')})
    return HttpResponse("%s(%s)"%(func,a))


    #return HttpResponse("%s({'name':('alex','alvin')})"%func)

    #return HttpResponse("%s('hello')"%func)
    #return HttpResponse("%s([12,34])"%func)
    #return HttpResponse("%s(5)"%func)
```
补充:
```
#views.py 中可以用  request.is_ajax() 方法判断是否是 ajax 请求，需要添加一个 HTTP 请求头：

#原生javascript：
#xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
#用 jQuery：
#用 $.ajax 方法代替 $.get，因为 $.get 在 IE 中不会发送 ajax header

#注意：is_ajax()在跨域ajax请求时不好使
```
