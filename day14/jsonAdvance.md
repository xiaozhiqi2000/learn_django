# 今天主要内容
[Ajax]()

## 一、Ajax 预备知识(json进阶)
### 1.什么是JSON
JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。JSON是用字符串来表示Javascript对象；

json字符串就是js对象的一种表现形式(字符串的形式),python的json模块，来测试下json字符串和json对象到底是什么

json中的引号一定是双引号
```
import json

i=10
s='hello'
t=(1,4,6)
l=[3,5,7]
d={'name':"python"}

json_str1=json.dumps(i)
json_str2=json.dumps(s)
json_str3=json.dumps(t)
json_str4=json.dumps(l)
json_str5=json.dumps(d)

print(json_str1)   #'10'
print(json_str2)   #'"hello"'
print(json_str3)   #'[1, 4, 6]'
print(json_str4)   #'[3, 5, 7]'
print(json_str5)   #'{"name": "python"}'
```
json_str就是json字符串；那么json字符串里都可以放哪些值呢？

JSON字符串内的值：
- 数字    （整数或浮点数）
- 字符串  （在双引号中）
- 逻辑值  （true 或 false）
- 数组    （在方括号中）
- 对象    （在花括号中，引号用双引）
- null     

这是js的数据对象；不管是python还是其它语言，它们都有自己的数据类型，但如果要处理成json字符串那么，就要把数据换转成js对应的数据对象

比如python的元组就被处理成了数组，字典就被处理成object，再加上引号就是咱们的json字符串了；

前端接受到json字符串，就可以通过JSON.parse()等方法解析成json对象(即js对象)直接使用了。

之所以称json对象为js的子集，是因为像undefined,NaN,{'name':'python'}等都不在json对象的范畴。

### 2.python与json对象的转换关系
在json的编码过程中，会存在从python原始类型向json类型的转换过程
```
python         -->        json
dict                      object
list,tuple                array
str,unicode               string
int,long,float            number
True                      true
False                     false
None                      null
```
举一个带方法的js对象
```
var person = {
    "name":"alex",
    "sex":"men",
    "teacher":{"name":"tiechui","sex":"half_men",},
    "bobby":['basketball','running'],
    "getName":function() {return 80;}
};

alert(person.name);
alert(person.getName());
alert(person.teacher.name);
alert(person.bobby[0]);
```
person是一个json对象，因为它满足json规范：在json六大范畴且引号双引！

### 3.js中json处理方法：parse()、stringify()
django中HttpResponse(json.dumps({'name':'python'})) 前端接收的json字符串需要用parse()方法转换成字符串
#### parse() 用于从一个json字符串中解析出json对象,如
```
var str = '{"name":"python","age":"23"}'
JSON.parse(str)     ------>  Object  {age: "23",name: "python"}
```
#### stringify()用于从一个json对象解析成json字符串，如
```
var c= {a:1,b:2} 
JSON.stringify(c)     ------>      '{"a":1,"b":2}'
```

注意1：单引号写在{}外，每个属性名都必须用双引号，否则会抛出异常。
注意2:
```
a={name:"python"};   //ok
b={'name':'python'}; //ok
c={"name":"python"}; //ok

alert(a.name);  //ok
alert(a[name]); //undefined
alert(a['name']) //ok
```
### 4.django向js发送数据
```
def login(request):
    obj={'name':"alex111"}
    return render(request,'index.html',{"objs":json.dumps(obj)})

----------------------------------

 <script>
     var temp={{ objs|safe }}
     alert(temp.name);
     alert(temp['name'])
 </script>
```
### 5.JSON与XML比较
- 可读性：   XML胜出；
- 解码难度：JSON本身就是JS对象（主场作战），所以简单很多；
- 流行度：   XML已经流行好多年，但在AJAX领域，JSON更受欢迎。

其实本没什么json对象，只是我们自己这么称呼罢了，所谓的json数据就是指json字符串，在前端解析出来的对象就是js对象的一部分

