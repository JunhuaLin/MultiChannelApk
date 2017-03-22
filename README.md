# MultiChannelApk
PackagingTools适用于多渠道android安装包apk生成，该工具的实现是基于美团分享的打包方式（[原文传送门](http://tech.meituan.com/mt-apk-packaging.html)）。简单，快捷，效率高。

## 使用环境
先要配置Python2.7（ubuntu和MacOS默认即可），因为PackagingTools运行在Python2.7上。

## 快速使用

### 代码
Android中加入如下代码：
```java
public class ChannelApplication extends Application {

    private static ChannelApplication INSTANCE;
    private static String CHANNEL = null;

    @Override
    public void onCreate() {
        super.onCreate();
        INSTANCE = this;
    }

    /**
     * 获取Channel信息
     *
     * @return String
     */
    public static String getChannel() {

        //应用运行中获取缓存CHANNEL
        if (CHANNEL != null) {
            return CHANNEL;
        }

        //首次打开应用获取
        ApplicationInfo appInfo = INSTANCE.getApplicationInfo();
        String sourceDir = appInfo.sourceDir;
        String result = "";
        ZipFile zipfile = null;
        try {
            zipfile = new ZipFile(sourceDir);
            Enumeration<?> entries = zipfile.entries();
            while (entries.hasMoreElements()) {
                ZipEntry entry = (ZipEntry) entries.nextElement();
                String entryName = entry.getName();
                System.out.println(entryName);
                if (entryName.startsWith("META-INF/channel_")) {
                    result = entryName;
                    break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (zipfile != null) {
                try {
                    zipfile.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        String[] split = result.split("_");
        if (split.length >= 2) {
            CHANNEL = result.substring(split[0].length() + 1);
        } else {
            CHANNEL = ""; //这里可以设置默认值
        }
        return CHANNEL;
    }
}
```


### 打包
#### 1.下载源文件
进入../MultiChannelApk/fun/目录运行：
>python packaging_tools.py -h

输出帮助信息：

![帮助信息](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/help.png)

按着帮助信息填写参数。

#### 2.设置源和渠道信息

![执行生成](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/gen.png)

- a 源：第一个位置参数 /home/junhua/channel/app-debug.apk
- c 渠道信息：/home/junhua/channel/ 即该目录下所有的*.channel文件（内部每行一条渠道信息且只能为**\w+**）

#### 3.生成文件

![生成文件](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/result1.png)

![APK内部文件](https://github.com/JunhuaLin/MultiChannelApk/blob/master/assets/inner.png)

### 使用Channel信息

>String channel = ChannelApplication.getChannel();
>System.out.println(channel);






