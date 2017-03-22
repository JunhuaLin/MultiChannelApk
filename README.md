# MultiChannelApk
PackagingTools适用于多渠道android安装包apk生成，该工具的实现是基于美团分享的打包方式（[原文传送门](http://tech.meituan.com/mt-apk-packaging.html)）。简单，快捷，效率高。

## 使用环境
先要配置Python2.7（ubuntu和MacOS默认即可），因为PackagingTools运行在Python2.7上。

## 快速使用

### 代码
Android中加入如下代码：



### 打包
#### 1.下载源文件
进入直接../MultiChannelApk/fun/packaging_tools.py运行：
>python packaging_tools.py -h

输出帮助信息：

![帮助信息](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/help.png)

按着帮助信息填写参数。

#### 2.设置源和渠道信息

![执行生成](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/gen.png)

源：第一个位置参数 /home/junhua/channel/app-debug.apk
渠道信息：/home/junhua/channel/ 即该目录下所有的*.channel文件

#### 3.生成文件

![生成文件](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/result1.png)




