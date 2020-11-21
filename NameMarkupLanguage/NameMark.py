from typing import Any, List

from NameMarkupLanguage.NameMarkDef import DefTag


class NameMark:
    sep = "#"
    tSep = "--"

    def __init__(self):
        self.__mPath__: str = ""
        self.__mName__: str = ""
        self.__mCategory__: str = ""
        self.__mID__: str = ""
        self.__mTag__: dict = {}
        self.__mDef__: bool = False
        self.__mDelete__: bool = False
        self.__mDefManager__ = None

    def name(self) -> str:
        return self.__mName__

    def path(self) -> str:
        return self.__mPath__

    def category(self) -> str:
        return self.__mCategory__

    def mid(self) -> str:
        return self.__mID__

    def tag(self) -> dict:
        return self.__mTag__

    def prop(self, prop: str) -> Any:
        if prop in self.__mTag__:
            PROP = self.__mTag__[prop]
            if isinstance(PROP, list):
                lst: List[str] = []
                for p in PROP:
                    if isinstance(p, DefTag) and not self.isDef():
                        if self.isDef():
                            rs = self.__mDefManager__.get(p, prop)
                            if isinstance(rs, list):
                                lst += rs
                            else:
                                lst.append(rs)
                        else:
                            lst.append(p.nmlId())
                    else:
                        lst.append(p)
                return lst
            elif isinstance(PROP, DefTag) and not self.isDef():
                return self.__mDefManager__.get(PROP, prop)
            else:
                return PROP

    def propNaked(self, prop: str) -> Any:
        if prop in self.__mTag__:
            PROP = self.__mTag__[prop]
            if isinstance(PROP, list):
                lst: List[str] = []
                for p in PROP:
                    if isinstance(p, DefTag):
                        lst.append(p.nmlId())
                    else:
                        lst.append(p)
                return lst
            elif isinstance(PROP, DefTag) and not self.isDef():
                return PROP.nmlId()
            else:
                return PROP

    def isDef(self):
        return self.__mDef__

    def nmlId(self) -> str:
        if self.category() == "" or self.category().isspace():
            return ""
        else:
            if self.mid() == "" or self.mid().isspace():
                return self.category()
            else:
                return self.sep.join([self.category(), self.mid()])

    def nmlDisplayId(self) -> str:
        return '[%s]' % self.nmlId()

    def setName(self, name: str):
        self.__mName__ = name

    def setPath(self, path: str):
        self.__mPath__ = path

    def setCategory(self, category: str):
        self.__mCategory__ = category

    def setId(self, mid: str):
        self.__mID__ = mid

    def setTag(self, tag: dict):
        self.__mTag__ = tag

    def setProp(self, prop: str, value):
        self.__mTag__[prop] = value

    def setDef(self, isDef):
        self.__mDef__ = isDef

    def setDefManager(self, defManager):
        self.__mDefManager__ = defManager
        if self.isDef() and self not in defManager:
            defManager.append(self)

    def addProp(self, prop: str, value: str):
        if prop in self.__mTag__:
            PROP = self.__mTag__[prop]
            if PROP is not None:
                if isinstance(PROP, list):
                    PROP.append(value)
                else:
                    self.setProp(prop, [PROP, value])
            else:
                self.setProp(prop, value)
        else:
            self.setProp(prop, value)

    def removeProp(self, prop: str):
        if prop in self.__mTag__:
            self.__mTag__.pop(prop)

    def removePropValue(self, prop: str, value: str):
        if prop in self.__mTag__:
            PROP = self.__mTag__[prop]
            if isinstance(PROP, list):
                if value in PROP:
                    PROP.remove(value)
            elif isinstance(PROP, str):
                if PROP == value:
                    self.__mTag__[prop] = ""

    def combineTag(self):
        s = ""
        for tag in self.__mTag__:
            value = self.__mTag__[tag]
            s = s + self.tSep + tag
            if isinstance(value, str):
                if value != "" and not value.isspace():
                    s = s + self.sep + value
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, DefTag):
                        s = s + '#[%s]' % v.nmlId()
                    elif isinstance(v, str):
                        if v != "" and not v.isspace():
                            s = s + self.sep + v
        return s

    def defManager(self) -> 'DefManager':
        return self.__mDefManager__

    def isValid(self):
        return self.__mName__ != "" and not self.__mName__.isspace() and self.combine() != ""

    def combine(self) -> str:
        if self.nmlId() != "":
            return '[%s]%s%s' % (self.nmlId(), self.name(), self.combineTag())
        else:
            return "%s%s" % (self.name(), self.combineTag())

    def combinePath(self) -> str:
        if not self.__mDef__:
            s = self.combine()
            import os
            dirname, filename = os.path.split(self.path())
            name, ext = os.path.splitext(self.path())
            s = os.path.join(dirname, s + ext)
            return s

    def isChanged(self) -> bool:
        if not self.__mDef__:
            return self.path() != self.combinePath()
        else:
            return True

    def isDelete(self) -> bool:
        return self.__mDelete__

    def delete(self) -> bool:
        self.__mDelete__ = True
        return self.__mDelete__

    def isFile(self) -> bool:
        import os
        return os.path.isfile(self.path())

    def undelete(self) -> bool:
        if self.isFile():
            self.__mDelete__ = False
            return False
        else:
            return True

    def commit(self) -> bool:
        import os

        if not self.isValid():
            raise Exception('Commit error: invalid object!')

        if self.isDef():
            if self.__mDefManager__ is None:
                raise Exception('Commit error: Can not found Def Manager!')
            return self.__mDefManager__.commit(self)

        if self.__mDelete__:
            if self.isFile():
                try:
                    os.remove(self.path())
                    self.setPath("")
                    return True
                except Exception as ex:
                    raise Exception('Commit error: ' + ex.__str__())
        else:
            if self.isChanged():
                try:
                    if os.path.isfile(self.path()):
                        os.rename(self.path(), self.combinePath())
                        self.setPath(self.combinePath())
                        return True
                    elif self.path() == "" or self.path().isspace():
                        # Creates a new file
                        with open(self.combinePath(), 'w') as fp:
                            pass
                            # To write data to new file uncomment
                            # this fp.write("New file created")
                        self.setPath(self.combinePath())
                        return True
                    else:
                        raise Exception('Commit error: ' + self.path() + " is invalid!")
                except Exception as ex:
                    raise Exception('Commit error: ' + ex.__str__())
        return False

    def __str__(self):
        return """{\n 'path': %s,\n 'nml': %s,\n 'isDef': %s \n}""" % (self.__mPath__, self.combine(), self.__mDef__)

    def __eq__(self, other):
        if isinstance(other, NameMark) and other is not None:
            return other.nmlId() == self.nmlId()
        else:
            return False

    def isSameFile(self, other: str):
        return other == self.path()
