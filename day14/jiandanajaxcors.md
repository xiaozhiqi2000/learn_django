### 支持跨域，简单请求

服务器设置响应头：Access-Control-Allow-Origin = '域名' 或 '*'
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
            xhr.open('GET', "http://c2.com:8000/test/", true);
            xhr.send();
        }

        function JqSendRequest(){
            $.ajax({
                url: "http://c2.com:8000/test/",
                type: 'GET',
                dataType: 'text',
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
    def get(self):
        self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        self.write('{"status": true, "data": "seven"}')
```
