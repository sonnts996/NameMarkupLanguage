from typing import List

from NameMarkupLanguage.NameMarkInterface import NameMark


class NMList:
    def __init__(self):
        self.__lst__: List['NameMark'] = []

    def append(self, nml: 'NameMark'):
        pass

    def remove(self, nml: 'NameMark'):
        pass

    def removeIndex(self, index: int):
        pass

    def removeId(self, nmlId: str):
        pass

    def count(self):
        pass

    def __getitem__(self, item) -> 'NameMark':
        if isinstance(item, int):
            return self.__lst__[item]
        elif isinstance(item, str):
            for nml in self.__lst__:
                if nml.nmlId() == item:
                    return nml

    def __contains__(self, item):
        return self.__lst__.__contains__(item)

    def __iter__(self):
        self.__inx__ = 0
        return self

    def __next__(self):
        if self.__inx__ < len(self.__lst__):
            a = self.__lst__[self.__inx__]
            self.__inx__ += 1
            return a
        else:
            raise StopIteration
