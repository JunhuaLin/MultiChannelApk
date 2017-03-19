# coding=utf-8
import os


class ChannelParser(object):
    def __init__(self):
        self.channels = []

    def parse(self, path):
        self.channels = []
        if not (path and os.path.exists(path)):
            return self.channels

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
        with open(path, "r") as f:

            while True:
                content = f.readlines(1000)
                if not content:
                    break

                for line in content:
                    line = line.strip()
                    if line:
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


if __name__ == "__main__":
    cp = ChannelParser()
    print cp.parse(r"D:\channel\1.txt")
