from typing import Any

import NameMarkupLanguage.NameMarkInterface as NMI


class NameMark:

    def __init__(self):
        self.__mPath__: str = ""
        self.__mName__: str = ""
        self.__mCategory__: str = ""
        self.__mID__: str = ""
        self.__mTag__: dict = {}
        self.__mDef__: bool = False
        self.__mDelete__: bool = False
        self.__mDefManager__: 'NMI.DefManager' = None

    def name(self) -> str:
        pass

    def path(self) -> str:
        pass

    def category(self) -> str:
        pass

    def mid(self) -> str:
        pass

    def tag(self) -> dict:
        pass

    def prop(self, prop: str) -> Any:
        pass

    def propNaked(self, prop: str) -> Any:
        pass

    def isDef(self):
        pass

    def defManager(self) -> 'NMI.DefManager':
        pass

    def nmlId(self) -> str:
        pass

    def nmlDisplayId(self) -> str:
        pass

    def setName(self, name: str):
        pass

    def setPath(self, path: str):
        pass

    def setCategory(self, category: str):
        pass

    def setId(self, mid: str):
        pass

    def setTag(self, tag: dict):
        pass

    def setProp(self, prop: str, value):
        pass

    def setDef(self, isDef: bool):
        pass

    def setDefManager(self, defManager: 'NMI.DefManager'):
        pass

    def addProp(self, prop: str, value: str):
        pass

    def removeProp(self, prop: str):
        pass

    def removePropValue(self, prop: str, value: str):
        pass

    def combineTag(self) -> str:
        pass

    def isValid(self):
        pass

    def combine(self) -> str:
        pass

    def combinePath(self) -> str:
        pass

    def isChanged(self) -> bool:
        pass

    def isDelete(self) -> bool:
        pass

    def delete(self) -> bool:
        pass

    def isFile(self) -> bool:
        pass

    def undelete(self) -> bool:
        pass

    def commit(self) -> bool:
        pass

    def isSameFile(self, other: str):
        pass

    def __str__(self):
        return """{\n 'path': %s,\n 'nml': %s,\n 'isDef': %s \n}""" % (self.__mPath__, self.combine(), self.__mDef__)

    def __eq__(self, other):
        if isinstance(other, NameMark) and other is not None:
            return other.nmlId() == self.nmlId()
        else:
            return False
