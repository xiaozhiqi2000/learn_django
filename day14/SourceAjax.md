# 今天主要内容
[原生Ajax]()

## 一、 AJAX核心（XMLHttpRequest）

其实AJAX就是在Javascript中多添加了一个对象：XMLHttpRequest对象。所有的异步交互都是使用XMLHttpRequest对象完成的。也就是说，我们只需要学习一个Javascript的新对象即可。

原生 Ajax 需要对不同浏览器做兼容，为了处理浏览器兼容，用以下方法来创建XMLHttpRequest对象
```
function createXMLHttpRequest() {
    var xmlHttp;
    // 适用于大多数浏览器，以及IE7和IE更高版本
    try{
        xmlHttp = new XMLHttpRequest();
    } catch (e) {
        // 适用于IE6
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            // 适用于IE5.5，以及IE更早版本
            try{
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e){}
        }
    }            
    return xmlHttp;
}

//大多数浏览器都支持DOM2规范
var xmlHttp = new XMLHttpRequest();
```
## 二、XMLHttpRequest 使用操作
### 1.打开与服务器的连接(open方法)
当得到XMLHttpRequest对象后，就可以调用该对象的open()方法打开与服务器的连接了。open()方法的参数如下：
```
open(method, url, async)：

method：请求方式，通常为GET或POST；
url：请求的服务器地址，例如：/ajaxdemo1/AServlet，若为GET请求，还可以在URL后追加参数；
async：这个参数可以不给，默认值为true，表示异步请求；
```
### 2.发送请求(send方法)
当使用open打开连接后，就可以调用XMLHttpRequest对象的send()方法发送请求了。send()方法的参数为POST请求参数，即对应HTTP协议的请求体内容，若是GET请求，需要在URL后连接参数。

注意：若没有参数，需要给出null为参数！若不给出null为参数，可能会导致FireFox浏览器不能正常发送请求！
```
xmlHttp.send(null);
```
### 3.接收服务器响应
当请求发送出去后，服务器端Servlet就开始执行了，但服务器端的响应还没有接收到。接下来我们来接收服务器的响应。

XMLHttpRequest对象有一个onreadystatechange事件，它会在XMLHttpRequest对象的状态发生变化时被调用。下面介绍一下XMLHttpRequest对象的5种状态：

- 0：初始化未完成状态，只是创建了XMLHttpRequest对象，还未调用open()方法；
- 1：请求已开始，open()方法已调用，但还没调用send()方法；
- 2：请求发送完成状态，send()方法已调用；
- 3：开始读取服务器响应；
- 4：读取服务器响应结束。 

onreadystatechange事件会在状态为1、2、3、4时引发。

下面代码会被执行四次！对应XMLHttpRequest的四种状态！
```
xmlHttp.onreadystatechange = function() {
    alert('hello');
};
```
但通常我们只关心最后一种状态，即读取服务器响应结束时，客户端才会做出改变。我们可以通过XMLHttpRequest对象的readyState属性来得到XMLHttpRequest对象的状态。
```
xmlHttp.onreadystatechange = function() {
    if(xmlHttp.readyState == 4) {
        alert('hello');    
    }
};
```
其实我们还要关心服务器响应的状态码是否为200，其服务器响应为404，或500，那么就表示请求失败了。我们可以通过XMLHttpRequest对象的status属性得到服务器的状态码。

最后，我们还需要获取到服务器响应的内容，可以通过XMLHttpRequest对象的responseText得到服务器响应内容。
```
xmlHttp.onreadystatechange = function() {
    if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        alert(xmlHttp.responseText);    
    }
};
```
### 4.发送POST请求：
1.需要设置请求头：xmlHttp.setRequestHeader(“Content-Type”, “application/x-www-form-urlencoded”)；

注意 :form表单会默认这个键值对;不设定，Web服务器会忽略请求体的内容。

2.在发送时可以指定请求体了：xmlHttp.send(“username=python&password=123”)

### 5.Ajax 实现小结
```
创建XMLHttpRequest对象；
调用open()方法打开与服务器的连接；
调用send()方法发送请求；
为XMLHttpRequest对象指定onreadystatechange事件函数，这个函数会在

XMLHttpRequest的1、2、3、4，四种状态时被调用；

XMLHttpRequest对象的5种状态，通常我们只关心4状态。

XMLHttpRequest对象的status属性表示服务器状态码，它只有在readyState为4时才能获取到。

XMLHttpRequest对象的responseText属性表示服务器响应内容，它只有在readyState为4时才能获取到！
```
### 6.原生Ajax实例(用户是否已经被注册)
#### (1)功能介绍

在注册表单中，当用户填写了用户名后，把光标移开后，会自动向服务器发送异步请求。服务器返回true或false，返回true表示这个用户名已经被注册过，返回false表示没有注册过。

客户端得到服务器返回的结果后，确定是否在用户名文本框后显示“用户名已被注册”的错误信息！

#### (2)案例分析
- 页面中给出注册表单；
- 在username表单字段中添加onblur事件，调用send()方法；
- send()方法获取username表单字段的内容，向服务器发送异步请求，参数为username；
- django 的视图函数：获取username参数，判断是否为“python”，如果是响应true，否则响应false
```
<script type="text/javascript">
        function createXMLHttpRequest() {
            try {
                return new XMLHttpRequest();
            } catch (e) {
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP");
                } catch (e) {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                }
            }
        }

        function send() {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.onreadystatechange = function() {
                if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    if(xmlHttp.responseText == "true") {
                        document.getElementById("error").innerText = "用户名已被注册！";
                        document.getElementById("error").textContent = "用户名已被注册！";
                    } else {
                        document.getElementById("error").innerText = "";
                        document.getElementById("error").textContent = "";
                    }
                }
            };
            xmlHttp.open("POST", "/ajax_check/", true, "json");
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            var username = document.getElementById("username").value;
            xmlHttp.send("username=" + username);
        }
</script>

//--------------------------------------------------index.html

<h1>注册</h1>
<form action="" method="post">
用户名：<input id="username" type="text" name="username" onblur="send()"/><span id="error"></span><br/>
密　码：<input type="text" name="password"/><br/>
<input type="submit" value="注册"/>
</form>


//--------------------------------------------------views.py
from django.views.decorators.csrf import csrf_exempt

def login(request):
    print('hello ajax')
    return render(request,'index.html')
    # return HttpResponse('hello python')

@csrf_exempt
def ajax_check(request):
    print('ok')

    username=request.POST.get('username',None)
    if username=='python':
        return HttpResponse('true')
    return HttpResponse('false')
```
