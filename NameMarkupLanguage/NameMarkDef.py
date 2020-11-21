sep = '#'
import_pattern = "#\[.*?#.*?\]"


def isDef(data: str) -> bool:
    import re
    return re.search(import_pattern, data) is not None


class DefTag:
    def __init__(self, nmlID="#"):
        self.__category__ = ""
        self.__mID__ = ""
        if nmlID.startswith('#['):
            nmlID = nmlID[2:]
        elif nmlID.startswith('['):
            nmlID = nmlID[1:]

        if nmlID.endswith(']'):
            nmlID = nmlID[:len(nmlID) - 1]

        if "#" in nmlID:
            data = nmlID.split("#", 1)
            self.__category__ = data[0]
            self.__mID__ = nmlID.replace(data[0] + '#', "", 1)
        else:
            self.__category__ = nmlID

    def category(self) -> str:
        return self.__category__

    def mid(self) -> str:
        return self.__mID__

    def nmlId(self) -> str:
        if self.category() == "" or self.category().isspace():
            return ""
        else:
            if self.mid() == "" or self.mid().isspace():
                return self.category()
            else:
                return sep.join([self.category(), self.mid()])

    def nmlDisplayId(self) -> str:
        return '#[%s]' % self.nmlId()

    def setCategory(self, category):
        self.__category__ = category

    def setId(self, mid):
        self.__mID__ = mid

    def __str__(self):
        return self.nmlId()

    def __eq__(self, other):
        if isinstance(other, DefTag):
            return other.nmlId() == self.nmlId()
        elif isinstance(other, str):
            return other == self.nmlId()
        else:
            return False
