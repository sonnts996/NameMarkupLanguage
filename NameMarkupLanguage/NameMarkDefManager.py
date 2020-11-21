from typing import Any, List

from NameMarkupLanguage import NMList
from NameMarkupLanguage.NameMark import NameMark
from NameMarkupLanguage.NameMarkDef import DefTag


class DefManager(NMList):

    def __init__(self):
        super().__init__()

    def append(self, xDef: NameMark):
        if xDef not in self.__lst__:
            super(DefManager, self).append(xDef)
            xDef.setDef(True)
            xDef.setDefManager(self)

    def get(self, nmlId: DefTag, prop: str = None) -> Any:
        if prop is None:
            for nml in self.__lst__:
                if nml.nmlId() == nmlId.nmlId():
                    return nml
        else:
            for nml in self.__lst__:
                if nml.nmlId() == nmlId.nmlId():
                    return nml.prop(prop)

    def isValid(self, nml: NameMark) -> bool:
        if nml.nmlId() != "" and not nml.nmlId().isspace():
            return nml.isValid()
        else:
            return False

    def commit(self, nml: NameMark) -> bool:
        if not self.isValid(nml):
            return False

        import os
        if nml.isDelete():
            self.remove(nml)
            if nml.isFile():
                try:
                    file1 = open(nml.path(), 'r', encoding='utf-8', errors='ignore')
                    rs: List[str] = file1.readlines()
                    file1.close()

                    for line in reversed(rs):
                        if line.startswith(nml.nmlId()):
                            rs.remove(line)

                    file2 = open(os.path.join(nml.path()), 'w', encoding='utf-8', errors='ignore')
                    file2.write("".join(rs))
                    file2.close()
                    return True
                except Exception as ex:
                    raise Exception("Edit NMDef error: " + str(ex))
        else:
            if nml.isFile():
                try:
                    file1 = open(nml.path(), 'r', encoding='utf-8', errors='ignore')
                    rs: List[str] = file1.readlines()
                    file1.close()

                    for line in reversed(rs):
                        if line.startswith(nml.nmlDisplayId()):
                            index = rs.index(line)
                            rs.remove(line)
                            rs.insert(index, nml.combine() + "\n")

                    file2 = open(nml.path(), 'w', encoding='utf-8', errors='ignore')
                    file2.write("".join(rs))
                    file2.close()
                    return True
                except Exception as ex:
                    raise Exception("Edit NMDef error: " + str(ex))
            elif nml.path() != "" and not nml.path().isspace():
                try:
                    file2 = open(nml.path(), 'w', encoding='utf-8', errors='ignore')
                    file2.write(nml.combine() + "\n")
                    file2.close()
                    return True
                except Exception as ex:
                    raise Exception("Edit NMDef error: " + str(ex))