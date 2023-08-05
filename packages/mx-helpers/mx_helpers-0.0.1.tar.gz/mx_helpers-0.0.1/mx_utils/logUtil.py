# -*- coding: utf-8 -*-
# @Time    : 2020/11/2 10:38 上午
# @Author  : X.Lin
# @Email   : ****
# @File    : logUtil.py
# @Software: IntelliJ IDEA
# @Desc    : 日志工具类.
import codecs
import datetime
import logging  # 引入logging模块
import os.path
import re
import time


class MultiprocessHandler(logging.FileHandler):
    """支持多进程的TimedRotatingFileHandler"""

    def __init__(self, filename, logPath='', when='D', backupCount=0, encoding=None, delay=False):
        """filename 日志文件名,when 时间间隔的单位,backupCount 保留文件个数
        delay 是否开启 OutSteam缓存
            True 表示开启缓存，OutStream输出到缓存，待缓存区满后，刷新缓存区，并输出缓存数据到文件。
            False表示不缓存，OutStrea直接输出到文件"""
        self.prefix = filename
        self.path = logPath
        self.backupCount = backupCount
        self.when = when.upper()
        # 正则匹配 年-月-日
        self.extMath = r"^\d{4}-\d{2}-\d{2}"

        # S 每秒建立一个新文件
        # M 每分钟建立一个新文件
        # H 每天建立一个新文件
        # D 每天建立一个新文件
        self.when_dict = {
            'S': "%Y-%m-%d-%H-%M-%S",
            'M': "%Y-%m-%d-%H-%M",
            'H': "%Y-%m-%d-%H",
            'D': "%Y-%m-%d"
        }
        # 日志文件日期后缀
        self.suffix = self.when_dict.get(when)
        if not self.suffix:
            raise ValueError(u"指定的日期间隔单位无效: %s" % self.when)
        # 拼接文件路径 格式化字符串
        self.filefmt = os.path.join(logPath, "%s.%s" % (self.prefix, self.suffix))
        # 使用当前时间，格式化文件格式化字符串
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        # 获得文件夹路径
        _dir = os.path.dirname(self.filefmt)
        try:
            # 如果日志文件夹不存在，则创建文件夹
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        except Exception:
            print(u"创建文件夹失败")
            print(u"文件夹路径：" + self.filePath)
            pass

        if codecs is None:
            encoding = None

        logging.FileHandler.__init__(self, self.filePath, 'a+', encoding, delay)

    def shouldChangeFileToWrite(self):
        """更改日志写入目的写入文件
        :return True 表示已更改，False 表示未更改"""
        # 以当前时间获得新日志文件路径
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        # 新日志文件日期 不等于 旧日志文件日期，则表示 已经到了日志切分的时候
        #   更换日志写入目的为新日志文件。
        # 例如 按 天 （D）来切分日志
        #   当前新日志日期等于旧日志日期，则表示在同一天内，还不到日志切分的时候
        #   当前新日志日期不等于旧日志日期，则表示不在
        # 同一天内，进行日志切分，将日志内容写入新日志内。
        if _filePath != self.filePath:
            self.filePath = _filePath
            return True
        return False

    def doChangeFile(self):
        """输出信息到日志文件，并删除多于保留个数的所有日志文件"""
        # 日志文件的绝对路径
        self.baseFilename = os.path.abspath(self.filePath)
        # stream == OutStream
        # stream is not None 表示 OutStream中还有未输出完的缓存数据
        if self.stream:
            # flush close 都会刷新缓冲区，flush不会关闭stream，close则关闭stream
            # self.stream.flush()
            self.stream.close()
            # 关闭stream后必须重新设置stream为None，否则会造成对已关闭文件进行IO操作。
            self.stream = None
        # delay 为False 表示 不OutStream不缓存数据 直接输出
        #   所有，只需要关闭OutStream即可
        if not self.delay:
            # 这个地方如果关闭colse那么就会造成进程往已关闭的文件中写数据，从而造成IO错误
            # delay == False 表示的就是 不缓存直接写入磁盘
            # 我们需要重新在打开一次stream
            # self.stream.close()
            self.stream = self._open()
        # 删除多于保留个数的所有日志文件
        print(self.backupCount)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                print('删除日志', s)
                try:
                    os.remove(s)
                except Exception as e:
                    print('删除日志失败. -- ' + str(e))

    def getFilesToDelete(self):
        """获得过期需要删除的日志文件"""
        # 分离出日志文件夹绝对路径
        # split返回一个元组（absFilePath,fileName)
        # 例如：split('I:\ScripPython\char4\mybook\util\logs\mylog.2017-03-19）
        # 返回（I:\ScripPython\char4\mybook\util\logs， mylog.2017-03-19）
        # _ 表示占位符，没什么实际意义，
        dirName, _ = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        print(dirName, self.baseFilename)
        result = []
        # self.prefix 为日志文件名 列如：mylog.2017-03-19 中的 mylog
        # 加上 点号 . 方便获取点号后面的日期
        prefix = self.prefix + '.'
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                # 日期后缀 mylog.2017-03-19 中的 2017-03-19
                suffix = fileName[plen:]
                # 匹配符合规则的日志文件，添加到result列表中
                if re.compile(self.extMath).match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()

        # 返回  待删除的日志文件
        #   多于 保留文件个数 backupCount的所有前面的日志文件。
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """发送一个日志记录
        覆盖FileHandler中的emit方法，logging会自动调用此方法"""
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class BaseLogs:

    def __init__(self, logName: str, logPath: str=None, isPrint: bool = True,
                 formatter: str = None):
        """

        :param logName: 日志名称,  系统日志/耗时日志/Debug日志 ...
        :param logPath: 日志路径. 绝对路径/相对路径.
        :param isPrint: 是否打印到控制台.
        """
        if not formatter:
            formatter = "%(asctime)s - [%(levelname)s] - %(filename)s[%(funcName)s:%(lineno)d] : %(message)s"

        self._mLogObj = logging.getLogger(logName)
        self._mLogObj.setLevel(logging.DEBUG if isPrint else logging.INFO)  # Log等级总开

        self._mDateStr = logName or 'default'  # 默认的日志名称.
        # 日志存储路径.
        self._mLogStoragePath = logPath # os.path.join(logPath, f'{logName}-logs/')
        fileSize = 10 * 1024 * 1024
        self._mFormatter = logging.Formatter(formatter)
        if self._mLogStoragePath:
            self.__mFh = MultiprocessHandler(logName, self._mLogStoragePath, when='D', backupCount=10, encoding='utf-8')
            self.__mFh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
            self.__mFh.setFormatter(self._mFormatter)
            self._mLogObj.addHandler(self.__mFh)

        if isPrint:  # 用于输出到控制台
            self.__mCh = logging.StreamHandler()
            self.__mCh.setLevel(logging.DEBUG)
            self.__mCh.setFormatter(self._mFormatter)
            self._mLogObj.addHandler(self.__mCh)

    def _createFolder(self):
        """ 创建指定名称的目录. """
        if not os.path.exists(self._mLogStoragePath):
            os.mkdir(self._mLogStoragePath)

    def getLogging(self):
        return self._mLogObj

# gSystemLog = BaseLogs('系统').getLogging()
# gRuntimeLog = _BaseLogs('耗时', isPrint=False).getLogging()   # 耗时日志记录不打印.
