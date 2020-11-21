from typing import Any, List

import NameMarkupLanguage.NameMarkInterface as NMI

sep = "#"
tSep = "--"


class NameMark(NMI.NameMark):

    def __init__(self):
        super(NameMark, self).__init__()

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
                    if isinstance(p, NMI.DefTag) and not self.isDef():
                        if self.isDef() and self.__mDefManager__ is not None:
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
            elif isinstance(PROP, NMI.DefTag) and not self.isDef() and self.__mDefManager__ is not None:
                return self.__mDefManager__.get(PROP, prop)
            else:
                return PROP

    def propNaked(self, prop: str) -> Any:
        if prop in self.__mTag__:
            PROP = self.__mTag__[prop]
            if isinstance(PROP, list):
                lst: List[str] = []
                for p in PROP:
                    if isinstance(p, NMI.DefTag):
                        lst.append(p.nmlId())
                    else:
                        lst.append(p)
                return lst
            elif isinstance(PROP, NMI.DefTag) and not self.isDef():
                return PROP.nmlId()
            else:
                return PROP

    def isDef(self):
        return self.__mDef__

    def defManager(self) -> NMI.DefManager:
        return self.__mDefManager__

    def nmlId(self) -> str:
        if self.category() == "" or self.category().isspace():
            if self.mid() == "" or self.mid().isspace():
                return ""
            else:
                return sep + self.mid()
        else:
            if self.mid() == "" or self.mid().isspace():
                return self.category()
            else:
                return sep.join([self.category(), self.mid()])

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

    def setDefManager(self, defManager:NMI.DefManager):
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
            s = s + tSep + tag
            if isinstance(value, str):
                if value != "" and not value.isspace():
                    s = s + sep + value
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, NMI.DefTag):
                        s = s + '#[%s]' % v.nmlId()
                    elif isinstance(v, str):
                        if v != "" and not v.isspace():
                            s = s + sep + v
        return s

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
        if self.path() == "" or self.path().isspace():
            self.__mDelete__ = False
        else:
            self.__mDelete__ = True
        return self.__mDelete__

    def isFile(self) -> bool:
        import os
        return os.path.isfile(self.path())

    def undelete(self) -> bool:
        if self.isFile() or self.path() == "" or self.path().isspace():
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
                    self.__mDelete__ = False
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

    def isSameFile(self, other: str):
        return other == self.path()
