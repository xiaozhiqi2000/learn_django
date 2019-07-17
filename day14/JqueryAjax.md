# 今天主要内容
[Jquery Ajax]()

## 一、 Jquery AJAX

jQuery其实就是一个JavaScript的类库，其将复杂的功能做了上层封装，使得开发者可以在其基础上写更少的代码实现更多的功能。
- jQuery 不是生产者，而是大自然搬运工。
- jQuery Ajax本质 XMLHttpRequest 或 ActiveXObject 

### 1.快捷API
```
$.get(url, [data], [callback], [type])
$.post(url, [data], [callback], [type])
$.getJSON(url, [data], [callback], [type])  #最主要是用来进行jsonp跨域操作的
$.getScript(url, [data], [callback])        #使用 AJAX 请求，获取和运行 JavaScript

url: 待载入页面的URL地址
data: 待发送 Key/value 参数。
success: 载入成功时回调函数。
dataType: 返回内容格式，xml, json,  script, text, html

function testGetScript() {
    $.getScript('test.js', function () {
    alert(add(1, 6));
    });
}

// test.js
function add(a,b){
    return a+b
}  
```
### 2.Jquery Ajax 核心API

'$.'ajax 详细用法及参数
```
url：请求地址
type：请求方式，GET、POST（1.9.0之后用method）
headers：请求头
data：要发送的数据
contentType：即将发送信息至服务器的内容编码类型(默认: "application/x-www-form-urlencoded; charset=UTF-8")
async：是否异步
timeout：设置请求超时时间（毫秒）

beforeSend：发送请求前执行的函数(全局)
success：成功之后执行的回调函数(全局)
error：失败之后执行的回调函数(全局)
complete：完成之后执行的回调函数(全局)
statusCode: 状态码
    $.ajax('/user/allusers', {

        success: function (data) {
            console.log(arguments);
        },

        error: function (jqXHR, textStatus, err) {

            // jqXHR: jQuery增强的xhr
            // textStatus: 请求完成状态
            // err: 底层通过throw抛出的异常对象，值与错误类型有关
            console.log(arguments);
        },

        complete: function (jqXHR, textStatus) {
            // jqXHR: jQuery增强的xhr
            // textStatus: 请求完成状态 success | error
            console.log('statusCode: %d, statusText: %s', jqXHR.status, jqXHR.statusText);
            console.log('textStatus: %s', textStatus);
        },

        statusCode: {
            '403': function (jqXHR, textStatus, err) {
                console.log(arguments);  //注意：后端模拟errror方式：HttpResponse.status_code=500
                
            },
            '400': function () {
            }
        }
    });    

accepts：通过请求头发送给服务器，告诉服务器当前客户端课接受的数据类型
dataType：将服务器端返回的数据转换成指定类型
    "xml": 将服务器端返回的内容转换成xml格式
    "text": 将服务器端返回的内容转换成普通文本格式
    "html": 将服务器端返回的内容转换成普通文本格式，在插入DOM中时，如果包含JavaScript标签，则会尝试去执行。
    "script": 尝试将返回值当作JavaScript去执行，然后再将服务器端返回的内容转换成普通文本格式
    "json": 将服务器端返回的内容转换成相应的JavaScript对象
    "jsonp": JSONP 格式

#使用 JSONP 形式调用函数时，如 "myurl?callback=?" jQuery 将自动替换 ? 为正确的函数名，以执行回调函数

#如果不指定，jQuery 将自动根据HTTP包MIME信息返回相应类型(an XML MIME type will yield XML, in 1.4 JSON will yield a JavaScript object, in 1.4 script will execute the script, and anything else will be returned as a string

converters： 转换器，将服务器端的内容根据指定的dataType转换类型，并传值给success回调函数
    $.ajax({
        accepts: {
          mycustomtype: 'application/x-some-custom-type'
        },
        
        // Expect a `mycustomtype` back from server
        dataType: 'mycustomtype'
    
        // Instructions for how to deserialize a `mycustomtype`
        converters: {
          'text mycustomtype': function(result) {
            // Do Stuff
            return newresult;
          }
        },
    });
```

### 3.Jquery Ajax 实例
dataType
```
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import json

def login(request):

    return render(request,'Ajax.html')


def ajax_get(request):

    l=['alex','little alex']
    dic={"name":"alex","pwd":123}

    #return HttpResponse(l)      #元素直接转成字符串alexlittle alex
    #return HttpResponse(dic)    #字典的键直接转成字符串namepwd
    return HttpResponse(json.dumps(l))
    return HttpResponse(json.dumps(dic))# 传到前端的是json字符串,要想使用,需要JSON.parse(data)

//---------------------------------------------------
    function testData() {

        $.ajax('ajax_get', {
           success: function (data) {
           console.log(data);
           console.log(typeof(data));
           //console.log(data.name);
           //JSON.parse(data);
           //console.log(data.name);
                                     },
           //dataType:"json",
                            }
                       )}

注解:Response Headers的content Type为text/html,所以返回的是String;但如果我们想要一个json对象
    设定dataType:"json"即可,相当于告诉ajax方法把服务器返回的数据转成json对象发送到前端.结果为object
    当然，
        return HttpResponse(json.dumps(a),content_type="application/json")

    这样就不需要设定dataType:"json"了。
    content_type="application/json"和content_type="json"是一样的！
```
dataFilter
```
function testData() {

    $.ajax('ajax_get', {
      success: function (data) {
          console.log(data);
       },

       dataType: 'json',
       dataFilter: function(data, type) {
           console.log(data);//["alex", "little alex"]
           console.log(type);//json
           //var tmp =  JSON.parse(data);
           return tmp.length;//2
       }
});}
```
beforesend
```
function testData() {
    $.ajax('ajax_get', {
     beforeSend: function (jqXHR, settings) {
            console.log(arguments);
            console.log('beforeSend');
            jqXHR.setRequestHeader('test', 'haha');
            jqXHR.testData = {a: 1, b: 2};
        },
        success: function (data) {
            console.log(data);
        },

        complete: function (xhr) {
            console.log(xhr);
            console.log(xhr.testData);
        },
})};
```
