# DeepOneRE  

基于pygame的deepone寝室播放器以及资源下载。  
不喜欢フラウ的玩家禁止使用😠

**使用方法：**  
1、获取寝室的json文件，将其放入json文件夹  
2、双击start.bat进入游戏,选择对应的寝室，load，等待下载后play  

**json文件的获取方式：**  
进入游戏的网页端，在浏览器中按F12，在network选项卡中的搜索栏搜索getResource，进入寝室，选择network选项卡中出现的getResource请求  
将响应内容复制到空白txt文件，将txt文件后缀改为json。  
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

`3.16`  
一些优化，包括播放的逻辑，射精动画的优化，还有文本的处理  
现在json文件只要格式正确会自动重命名  
机翻暂时移除  
添加了一个bat，请使用start.bat启动游戏  

`3.18`  
修复了动画帧数的问题  
修复了json文件重命名的错误  
修复了视频不能正确结束的bug  
添加了机翻，以及机翻缓存，现在会优先加载缓存里的翻译文本  
修复了libmpg123-0.dll缺失的问题（新的打包命令）  

`5.10`  
移除了百度翻译的接口，改为使用[DeepOne_translate_CN](https://github.com/Lisanjin/DeepOne_translate_CN)提供的gpt翻译  

`25.4.5`  
添加了一个把hs导出为mp4的功能，目前只支持导出静态的hs，需要ffmpeg