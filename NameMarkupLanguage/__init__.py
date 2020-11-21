import os
import re
from typing import List

import packaging_tutorial.NameMarkupLanguage.NameMarkDef as XDef
from packaging_tutorial.NameMarkupLanguage.NameMark import NameMark
from packaging_tutorial.NameMarkupLanguage.NameMarkList import NMList
from packaging_tutorial.NameMarkupLanguage.NameMarkDefManager import DefManager

category_pattern = "\[.*?\]"


def init() -> NameMark:
    return NameMark()


def buildPath(path: str, defManager: DefManager = None) -> NameMark:
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    nml = __NMLString__(name)
    nml.setDefManager(defManager)
    nml.setPath(path)
    nml.setDef(False)
    return nml


def buildDef(defPath, data: str) -> NameMark:
    nml = __NMLString__(data)
    nml.setPath(defPath)
    nml.setDef(True)
    return nml


def __NMLString__(name: str) -> NameMark:
    nml = NameMark()
    if name != "" and not name.isspace():
        section = name.split(NameMark.tSep)
        firstSection = ""
        lastSection = []
        if len(section) > 0:
            firstSection = section[0]
            if len(section) > 1:
                lastSection = section[1:]

        if firstSection == "" or firstSection.isspace():
            return nml
        else:
            if firstSection.startswith("["):
                nmlIds = re.findall(category_pattern, firstSection)
                if len(nmlIds) > 0:
                    nmlId: str = nmlIds[0]
                    if nmlId.startswith("["):
                        nmlId = nmlId[1:]
                    if nmlId.endswith("]"):
                        nmlId = nmlId[: len(nmlId) - 1]
                    if NameMark.sep in nmlId:
                        data = nmlId.split(NameMark.sep)
                        if len(data) > 0:
                            nml.setCategory(data[0])
                            mid = nmlId.replace(data[0] + NameMark.sep, "", 1)
                            nml.setId(mid)
                    else:
                        nml.setCategory(nmlId)
                    nmlName = firstSection.replace("[%s]" % nmlId, "", 1)
                    nml.setName(nmlName)
                else:
                    nml.setName(firstSection)
            else:
                nml.setName(firstSection)

        tag = {}
        for sec in lastSection:
            if not sec.startswith("#"):
                if NameMark.sep in sec:
                    imps = re.findall(XDef.import_pattern, sec)
                    for imp in imps:
                        sec = sec.replace(imp, "")

                    tags = sec.split(NameMark.sep)
                    tag[tags[0]] = []
                    for imp in imps:
                        xDef = XDef.DefTag(imp)
                        tags.append(xDef)
                    if len(tags) > 1:
                        for t in tags[1:]:
                            tag[tags[0]].append(t)
                else:
                    tag[sec] = ""

        nml.setTag(tag)
    return nml


def load(path: str, filters: list = None) -> NMList:
    nmlList = NMList()
    defManager = DefManager()
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == ".xdef":
                defPath = os.path.join(root, file)
                lstDef = readDef(defPath)
                for d in lstDef:
                    defManager.append(buildDef(defPath, d.replace("\n", "")))
            else:
                if filters is not None and file_extension in filters:
                    nmlList.append(buildPath(os.path.join(root, file), defManager))
                elif filters is None:
                    nmlList.append(buildPath(os.path.join(root, file), defManager))
    return nmlList


def readDef(path: str) -> List[str]:
    rs: List[str] = []
    try:
        file1 = open(os.path.join(path), 'r', encoding='utf-8', errors='ignore')
        rs = file1.readlines()
        return rs
    except Exception as ex:
        print(ex)
        return rs


def findWithCategory(data: NMList, category: str, case=False) -> NMList:
    lst = NMList()
    for nml in data:
        if nml.category() == category if case else nml.name().lower() == category.lower():
            lst.append(nml)
    return lst


def findWithName(data: NMList, query: str, case=False) -> NMList:
    lst = NMList()
    for nml in data:
        if query in nml.name() if case else query.lower() in nml.name().lower():
            lst.append(nml)
    return lst


def findWithTag(data: NMList, tag, value: str, case=False, equal=False) -> NMList:
    lst = NMList()
    for nml in data:
        if tag in nml.tag():
            tags = nml.prop(tag)
            if isinstance(tags, list):
                for t in tags:
                    pass
            elif isinstance(tags, str):
                if case:
                    if tags == value if equal else value in tags:
                        lst.append(nml)
                else:
                    if tags.lower() == value.lower() if equal else value.lower() in tags.lower():
                        lst.append(nml)
    return lst


def findWithID(data: NMList, nmlID: str) -> NameMark:
    for nml in data:
        if nml.nmlId() == nmlID:
            return nml


def checkIdDuplicate(data: NMList, nmlID: str) -> NMList:
    lst = NMList()
    for nml in data:
        if nml.nmlId() == nmlID:
            lst.append(nml)
    return lst


def nextId(data: NMList, category: str, index: int = 0, fill=False, idFormat="%d") -> str:
    lst = findWithCategory(data, category, True)
    if not fill:
        index = lst.count()
    newId = category + NameMark.sep + idFormat % index
    lstId = checkIdDuplicate(lst, newId)
    if lstId.count() == 0:
        return newId
    else:
        return nextId(data, category, index + 1, True, idFormat)
