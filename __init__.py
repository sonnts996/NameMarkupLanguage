import NameMarkupLanguage as NML


def main():
    listNameMark = NML.load('C:\\Users\\DEV-C2-2\\XuCompa\\XRequest\\Request')
    nml = listNameMark[0]
    nml.setCategory("Hello")
    nml.commit()
    mng = nml.defManager()

    new = NML.NameMark()
    new.setPath("C:\\Users\\DEV-C2-2\\XuCompa\\XRequest\\Request\\test.xdef")
    new.setDef(True)
    new.setCategory("Test")
    new.setId("01")
    new.setName("hello")
    new.setDefManager(mng)
    new.commit()
    print("Check Point")


if __name__ == '__main__':
    main()
