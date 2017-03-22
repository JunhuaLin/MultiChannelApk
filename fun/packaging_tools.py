# coding=utf-8
import argparse
import os
import re
import shutil
import zipfile

import time


class PackagingListener(object):
    def on_start(self, channel_count):
        pass

    def on_pack(self, message):
        pass

    def on_error(self, message):
        pass

    def on_finish(self):
        pass


class PrintPackagingListener(PackagingListener):
    def __init__(self):
        self.start_time = time.time()
        self.count = 0
        self.end_time = 0

    def on_start(self, channel_count):
        self.count = channel_count
        print "start at ", self.start_time
        print "count ", channel_count

    def on_pack(self, message):
        print message[0], str(message[1]) + "/" + str(self.count), message[2]

    def on_error(self, message):
        print message

    def on_finish(self):
        self.end_time = time.time()
        print "finished at ", self.end_time
        print "time %.3fs" % (self.end_time - self.start_time)


class ChannelParser(object):
    """
    用于解析渠道文件信息，渠道信息存储在以".channel"为扩展名的文本文件中，且为UTF-8无BOM编码。
    """

    def __init__(self):
        self.channels_dict = dict()

    def parse(self, path):
        if not (path and os.path.exists(path)):
            return self.channels_dict

        try:
            if os.path.isfile(path):
                self._parse_file(path)
            elif os.path.isdir(path):
                self._parse_dir(path)
        except:
            pass
        return self.channels_dict

    def _parse_file(self, path):
        """
        读取.channel文件的渠道信息
        :param path: 文件路径
        """
        if not (path and os.path.exists(path) and os.path.isfile(path) and path.endswith(".channel")):
            return

        set_name = os.path.split(os.path.splitext(path)[0])[1]
        temp_channels = set()
        patten = re.compile(r"[\w]+")
        with open(path, "r") as f:
            while True:
                content = f.readlines()
                for line in content:
                    line = line.strip()
                    if patten.match(line):
                        temp_channels.add(line)

                if not content:
                    break

        if set_name in self.channels_dict:
            self.channels_dict[set_name].update(temp_channels)
        else:
            self.channels_dict[set_name] = temp_channels

    def _parse_dir(self, path):
        """
        返回path路径中的channel信息
        :param path:路径
        """
        if not (path and os.path.exists(path) and os.path.isdir(path)):
            return

        name_list = os.listdir(path)
        for value in name_list:
            file_or_dir = os.path.join(path, value)
            if os.path.isfile(file_or_dir):
                self._parse_file(file_or_dir)
            elif os.path.isdir(file_or_dir):
                self._parse_dir(file_or_dir)


class ApkPackager(object):
    """
    用于将渠道信息压入apk文件中
    """

    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.channel_dict = dict()
        self.output_path = ""
        self.split_state = False
        self.listener = None
        self.prefix_str = ""
        self.suffix_str = ""

    @staticmethod
    def instance(apk_path):
        return ApkPackager(apk_path)

    def channels(self, channel_path):
        self.channel_dict = ChannelParser().parse(channel_path)
        return self

    def split(self, split_state):
        """
        是否按不同channel文件分开存储
        :param split_state:
        :return:
        """
        self.split_state = split_state
        return self

    def dist(self, output_path):
        self.output_path = output_path
        return self

    def prefix(self, prefix_str):
        """
        前缀仅作用于apk文件名称中
        :param prefix_str:
        :return:
        """
        self.prefix_str = prefix_str
        return self

    def suffix(self, suffix_str):
        """
        后缀仅作用于apk文件名称中
        :param suffix_str:
        :return:
        """
        self.suffix_str = suffix_str
        return self

    def pack(self, listener=None):
        """
        向apk中写入META-INF/channel_{channel}空文件，channel为[\w+]的渠道名
        :param listener:
        :return:
        """
        if listener:
            self.listener = listener
        else:
            self.listener = PrintPackagingListener()

        if not (self.apk_path and os.path.exists(self.apk_path) and self.apk_path.endswith(".apk")):
            self.listener.on_error("you must select apk!")
            return

        count = 0
        for channels in self.channel_dict.itervalues():
            count += len(channels)
        self.listener.on_start(count)

        if "" == self.output_path:
            output = os.path.split(self.apk_path)
            apk_dir = os.path.join(output[0], "apk")
            if not os.path.exists(apk_dir):
                os.makedirs(apk_dir)
            self.output_path = apk_dir
        else:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

        now_index = 0
        for set_name, channel_set in self.channel_dict.iteritems():
            temp_output_path = self.output_path
            if self.split_state:
                temp_output_path = os.path.join(self.output_path, set_name)
                if not os.path.exists(temp_output_path):
                    os.makedirs(temp_output_path)

            for channel in channel_set:
                output_apk = os.path.join(temp_output_path,
                                          "".join([self.prefix_str, channel, self.suffix_str, ".apk"]))
                shutil.copyfile(self.apk_path, output_apk)

                with zipfile.ZipFile(output_apk, 'a', zipfile.ZIP_DEFLATED) as zipped:
                    empty_channel_file = "META-INF/channel_{channel}".format(channel=channel)
                    zipped.write(self.apk_path, empty_channel_file)

                now_index += 1
                self.listener.on_pack((set_name, now_index, output_apk))

        self.listener.on_finish()


def main():
    parse = argparse.ArgumentParser(description=u"packaging_tools用于生成多渠道Apk")
    parse.add_argument("a", type=str, help=u"模版apk的路径")
    parse.add_argument("c", type=str, help=u"渠道信息文件(*.channel)或文件夹的路径")
    parse.add_argument("-o", "--output", type=str, default="",
                       help=u"存储生成含有渠道信息Apk的文件夹路径，默认存储在模版apk目录下apk文件夹内")
    parse.add_argument("-p", "--prefix", type=str, help=u"生成apk文件名称的前缀", default="")
    parse.add_argument("-s", "--suffix", type=str, help=u"生成apk文件名称的后缀", default="")
    parse.add_argument("-sp", "--split", type=int, choices=[0, 1],
                       default=0, help=u"0所有生成的apk存在同一个文件夹内，1按不同channel文件分开存储")

    args = parse.parse_args()

    (ApkPackager
     .instance(args.a)
     .channels(args.c)
     .split(args.split == 1)
     .dist(args.output)
     .prefix(args.prefix)
     .suffix(args.suffix)
     .pack())


if __name__ == "__main__":
    main()
