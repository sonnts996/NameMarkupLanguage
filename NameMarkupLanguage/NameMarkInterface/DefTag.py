class DefTag:
    def __init__(self):
        self.__category__ = ""
        self.__mID__ = ""

    def category(self) -> str:
        pass

    def mid(self) -> str:
        pass

    def nmlId(self) -> str:
        pass

    def nmlDisplayId(self) -> str:
        pass

    def setCategory(self, category):
        pass

    def setId(self, mid):
        pass

    def __str__(self):
        return self.nmlId()

    def __eq__(self, other):
        if isinstance(other, DefTag):
            return other.nmlId() == self.nmlId()
        elif isinstance(other, str):
            return other == self.nmlId()
        else:
            return False
