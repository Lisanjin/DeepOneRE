# DeepOneRE  

基于pygame的deepone寝室播放器以及资源下载。  
不喜欢フラウ的玩家禁止使用😠

**使用方法：**  
1、获取寝室的json文件，将其放入json文件夹  
2、进入游戏选择对应的json，load，等待下载后play

**json文件的获取方式：**  
进入游戏的网页端，在浏览器中按F12，在network选项卡中的搜索栏搜索getResource，进入寝室，选择network选项卡中出现的getResource请求  

将响应内容复制到空白txt文件，文件名命名为内容中storyIds后面[]中的编号，storyIds重复冲突的话（动态静态寝室id会重名）再在id后面加个_区分，将txt文件后缀改为json。  

还是不会的话参考这个[视频](https://www.bilibili.com/video/BV1oC4y1z75d/)

`5.27`  
添加了百度的机翻，需要的请自行申请api（免费），[申请教程](https://docs2.ayano.top/#/4.0/basic/translate?id=%e7%99%be%e5%ba%a6%e7%bf%bb%e8%af%91%e6%8e%a5%e5%8f%a3)  
程序里附带的apikey是无效的，只是给笨蛋们提供一个照抄的填写格式

`7.3`  
添加自定义设置，添加多线程下载  

`10.13`  
修复了一个文本刷新的错误  
添加了对芙拉黑子的惩罚措施  
添加了程序icon和一个打包命令

`1.15`  
修改了hs列表的显示 
现在会使用预览图来显示hs列表 

