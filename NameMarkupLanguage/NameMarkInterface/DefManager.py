from typing import Any

from NameMarkupLanguage.NameMarkInterface import NameMark, DefTag, NMList


class DefManager(NMList):

    def __init__(self):
        super(DefManager, self).__init__()

    def get(self, nmlId: 'DefTag', prop: str = None) -> Any:
        pass

    def isValid(self, nml: 'NameMark') -> bool:
        pass

    def commit(self, nml: 'NameMark') -> bool:
        pass
