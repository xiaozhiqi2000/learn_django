### 跨域传输cookie

在跨域请求中，默认情况下，HTTP Authentication信息，Cookie头以及用户的SSL证书无论在预检请求中或是在实际请求都是不会被发送。

如果想要发送：
- 浏览器端：XMLHttpRequest的withCredentials为true
- 服务器端：Access-Control-Allow-Credentials为true
- 注意：服务器端响应的 Access-Control-Allow-Origin 不能是通配符 *
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

            xhr.withCredentials = true;

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
                xhrFields:{withCredentials: true},
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
        self.set_header('Access-Control-Allow-Credentials', "true")
        
        self.set_header('xxoo', "seven")
        self.set_header('bili', "daobidao")
        self.set_header('Access-Control-Expose-Headers', "xxoo,bili")

        self.set_cookie('kkkkk', 'vvvvv');

        self.write('{"status": true, "data": "seven"}')

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        self.set_header('Access-Control-Allow-Headers', "k1,k2")
        self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        self.set_header('Access-Control-Max-Age', 10)
```
