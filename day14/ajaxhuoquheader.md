### 跨域获取响应头

默认获取到的所有响应头只有基本信息，如果想要获取自定义的响应头，则需要再服务器端设置Access-Control-Expose-Headers。

```
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>

    <p>
        <input type="submit" onclick="XmlSendRequest();" />
    </p>

    <p>
        <input type="submit" onclick="JqSendRequest();" />
    </p>

    <script type="text/javascript" src="jquery-1.12.4.js"></script>
    <script>
        function XmlSendRequest(){
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function(){
                if(xhr.readyState == 4) {
                    var result = xhr.responseText;
                    console.log(result);
                    // 获取响应头
                    console.log(xhr.getAllResponseHeaders());
                }
            };
            xhr.open('PUT', "http://c2.com:8000/test/", true);
            xhr.setRequestHeader('k1', 'v1');
            xhr.send();
        }

        function JqSendRequest(){
            $.ajax({
                url: "http://c2.com:8000/test/",
                type: 'PUT',
                dataType: 'text',
                headers: {'k1': 'v1'},
                success: function(data, statusText, xmlHttpRequest){
                    console.log(data);
                    // 获取响应头
                    console.log(xmlHttpRequest.getAllResponseHeaders());
                }
            })
        }


    </script>
</body>
</html>
``` 
tornado 服务端
```
class MainHandler(tornado.web.RequestHandler):
    
    def put(self):
        self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        self.set_header('xxoo', "seven")
        self.set_header('bili', "daobidao")
        self.set_header('Access-Control-Expose-Headers', "xxoo,bili")
        self.write('{"status": true, "data": "seven"}')

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        self.set_header('Access-Control-Allow-Headers', "k1,k2")
        self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        self.set_header('Access-Control-Max-Age', 10)
```
