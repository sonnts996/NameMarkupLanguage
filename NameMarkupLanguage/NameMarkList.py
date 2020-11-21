from typing import List

from packaging_tutorial.NameMarkupLanguage.NameMark import NameMark


class NMList:
    def __init__(self):
        self.__lst__: List[NameMark] = []

    def append(self, nml: NameMark):
        self.__lst__.append(nml)

    def remove(self, nml: NameMark):
        if nml in self.__lst__:
            self.__lst__.remove(nml)

    def removeIndex(self, index: int):
        if index < len(self.__lst__):
            nml = self.__lst__[index]
            self.__lst__.remove(nml)

    def removeId(self, nmlId: str):
        for nml in self.__lst__:
            if nml.nmlId() == nmlId:
                self.__lst__.remove(nml)
                break

    def count(self):
        return len(self.__lst__)

    def __getitem__(self, item) -> NameMark:
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
