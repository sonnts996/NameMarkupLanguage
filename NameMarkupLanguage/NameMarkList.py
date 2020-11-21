import NameMarkupLanguage.NameMarkInterface as  NMI


class NMList(NMI.NMList):

    def __init__(self):
        super(NMList, self).__init__()

    def append(self, nml: NMI.NameMark):
        self.__lst__.append(nml)

    def remove(self, nml: NMI.NameMark):
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
