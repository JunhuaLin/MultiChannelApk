# coding=utf-8
import os
import re
import shutil
import zipfile


class ChannelParser(object):
    def __init__(self):
        self.channels = []

    def parse(self, path):
        self.channels = []
        if not (path and os.path.exists(path)):
            return []

        try:
            if os.path.isfile(path):
                self.channels.extend(self._parse_file(path))
            elif os.path.isdir(path):
                self.channels.extend(self._parse_dir(path))
        except:
            pass
        return self.channels

    def _parse_file(self, path):
        """
        读取.txt文件的渠道信息
        :param path: 文件路径
        :return:信息集合
        """
        if not (path and os.path.exists(path) and os.path.isfile(path) and path.endswith(".txt")):
            return []

        temp_channels = []
        patten = re.compile(r"[\w]+")
        with open(path, "r") as f:

            while True:
                content = f.readlines(1000)
                if not content:
                    break

                for line in content:
                    line = line.strip()
                    if line and patten.match(line):
                        temp_channels.append(line)

        return temp_channels

    def _parse_dir(self, path):
        """
        返回path路径中的channel信息
        :param path:路径
        :return:信息集合
        """
        temp_channels = []
        if not (path and os.path.exists(path) and os.path.isdir(path)):
            return temp_channels

        name_list = os.listdir(path)
        for value in name_list:
            file_or_dir = os.path.join(path, value)
            if os.path.isfile(file_or_dir):
                temp_channels.extend(self._parse_file(file_or_dir))
            elif os.path.isdir(file_or_dir):
                temp_channels.extend(self._parse_dir(file_or_dir))

        return temp_channels


class PackagingApk(object):
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.channel_list = []
        self.output_path = ""

    @staticmethod
    def instance(apk_path):
        return PackagingApk(apk_path)

    def channels(self, channel_path):
        self.channel_list = ChannelParser().parse(channel_path)
        return self

    def dist(self, output_path):
        self.output_path = output_path
        return self

    def pack(self, prefix="", suffix=""):
        """
        向apk中写入META-INF/channel_{channel}空文件，channel为ascii渠道名
        :param prefix:
        :param suffix:
        :return:
        """
        if not self.output_path:
            output = os.path.split(self.apk_path)
            apk_dir = os.path.join(output[0], "apk")
            if not os.path.exists(apk_dir):
                os.makedirs(apk_dir)
            self.output_path = apk_dir

        for channel in self.channel_list:
            output_apk = os.path.join(self.output_path,
                                      "".join([prefix, channel, suffix, ".apk"]))
            shutil.copyfile(self.apk_path, output_apk)

            with zipfile.ZipFile(output_apk, 'a', zipfile.ZIP_DEFLATED) as zipped:
                empty_channel_file = "META-INF/channel_{channel}".format(channel=channel)
                zipped.write(self.apk_path, empty_channel_file)


if __name__ == "__main__":
    your_apk = r"D:\channel\app-debug.apk"
    channel_file = r"D:\channel"

    PackagingApk.instance(your_apk).channels(channel_file).pack()
