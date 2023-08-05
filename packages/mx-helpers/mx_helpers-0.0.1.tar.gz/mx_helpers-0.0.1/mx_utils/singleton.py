# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 2:18 下午
# @Author  : X.Lin
# @Email   : ****
# @File    : singleton.py
# @Software: PyCharm
# @Desc    : 单例模式继承类.

class _MySingletonType(type):

    def __init__(self, name, bases, attre):
        super().__init__(name, bases, attre)
        self.instance = None

    def __call__(self, *args, **kwargs):
        if not self.instance:
            self.instance = self.__new__(self)
            self.__init__(self.instance, *args, **kwargs)

        return self.instance


class Singleton(object, metaclass=_MySingletonType):
    pass
