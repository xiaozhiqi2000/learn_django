### 支持跨域，复杂请求

由于复杂请求时，首先会发送“预检”请求，如果“预检”成功，则发送真实数据。
- “预检”请求时，允许请求方式则需服务器设置响应头：Access-Control-Request-Method
- “预检”请求时，允许请求头则需服务器设置响应头：Access-Control-Request-Headers
- “预检”缓存时间，服务器设置响应头：Access-Control-Max-Age
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
        self.write('{"status": true, "data": "seven"}')

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        self.set_header('Access-Control-Allow-Headers', "k1,k2")
        self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        self.set_header('Access-Control-Max-Age', 10)
```

