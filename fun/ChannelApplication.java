package cn.junhua.android.linjhandroid;

import android.app.Application;
import android.content.pm.ApplicationInfo;

import java.io.IOException;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * Created by junhua on 17-3-22.
 */
public class ChannelApplication extends Application {

    private static ChannelApplication INSTANCE;
    private static String CHANNEL = null;

    @Override
    public void onCreate() {
        super.onCreate();
        INSTANCE = this;

        getChannel();
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

        ApplicationInfo appInfo = INSTANCE.getApplicationInfo();
        //首次打开应用获取或者清空缓存后获取
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
