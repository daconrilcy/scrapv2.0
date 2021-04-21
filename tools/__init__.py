import threading
import glob,os


def makeUnikList(listeBrute: list):
    if (listeBrute is None) | (len(listeBrute) == 0):
        return listeBrute

    listUnique = []
    for data in listeBrute:
        if not data in listUnique:
            listUnique.append(data)
    return listUnique


def dataNotNull(data):
    if data is None:
        return False
    if isinstance(data, str):
        if data == "":
            return False
    if isinstance(data, (int, float)):
        if data == 0:
            return False
    if isinstance(data, (list, dict)):
        if len(data) == 0:
            return False
    return True


def importer(source: str, functionToWeb, functionToFile):
    if source.lower() == "web":
        functionToWeb()
    else:
        functionToFile()


def compterPages_nRefTot_NRefPPage(nrefTotal: int, nrefPerPage: int):
    totalpage = 1
    if nrefPerPage != 0:
        if nrefTotal % nrefPerPage > 0:
            totalpage = int(nrefTotal // nrefPerPage + 1)
        else:
            totalpage = int(nrefTotal // nrefPerPage)

    return totalpage


def varToArg(var, index):
    result = []
    if isinstance(var, int):
        if not isinstance(index, str):
            addMessage('votre variable est in int donc votre index doit être unique')
        else:
            for i in range(0, var):
                result.append({index: i})

    return result


def threader(nThread: int, function, args, addedText: str = None, messageIntermediare: bool = None):
    if not dataNotNull(addedText):
        addedText = " datas traitées"
    if messageIntermediare is None:
        messageIntermediare = False

    th = []
    receveur = []
    container = []
    for n in range(0, nThread):
        container.append([])
        arg = args[n]
        th.append(threading.Thread(target=function, args=(arg, container[n])))
        th[n].start()

    nvalue = 0
    for n in range(0, nThread):
        th[n].join()
        lcont = len(container[n])
        nvalue += lcont
        if messageIntermediare:
            addMessageN(lcont, addedText)
        receveur.extend(container[n])
    addMessage("----------------")
    addMessageN(nvalue, addedText)

    return receveur


def addMessageN(n: (int,float), addedmessage: str):
    if not addedmessage[0:1] == " ":
        addedmessage = " " + addedmessage
    addMessage(str(n) + addedmessage)


def addMessage(message):
    print(message)


def isInListe(data, listToCheck):
    for e in listToCheck:
        if data == e:
            return True
    return False


def isInListeDetailled(data, listToCheck):
    result = {"result": False, "index": None, 'keys': None}
    for i in range(len(listToCheck)):
        if isinstance(listToCheck[i], dict):
            for k in listToCheck[i].keys():
                if data == listToCheck[i][k]:
                    result['result']= True
                    result["index"] = i
                    result['keys'] = k
                    break
        elif data in listToCheck[i]:
            result['result'] = True
            result['index'] = i
            break
    return result


def isInKeyReturnIndex(dataToFind, listToLook: list, keyName: str):
    result = {"result": False, "index": None}
    sublist = []
    if len(listToLook) > 0:
        for i in range(len(listToLook)):
            if isinstance(listToLook[i], (list, dict)):
                if keyName in listToLook[i].keys():
                    sublist.append(listToLook[i][keyName])
                else:
                    sublist.append("")
            elif isinstance(listToLook[i], object):
                sublist.append(listToLook[i].__getattribute__(keyName))

    if len(sublist) > 0:
        for i in range(len(sublist)):
            if sublist[i] == dataToFind:
                result['result'] = True
                result['index'] = i
                break

    return result


def cutListInN(listToCut: list, ncut: int):
    if (ncut == 0) | (not dataNotNull(listToCut)):
        return listToCut

    result = []
    ld = len(listToCut)
    reste = ld % ncut

    if reste >= ld:
        ncut = ld
        reste = 0

    if ncut <= 1:
        ncut = 1

    if reste != 0:
        if reste >= ncut-1:
            lseg = ld//ncut + 1
            lseg2 = ld -(ncut - 1)*lseg
        else:
            lseg = ld // ncut
            lseg2 = lseg + 1
    else:
        lseg = ld//ncut
        lseg2 = lseg

    for c in range(0, ncut-reste):
        result.append([])
        for i in range(lseg):
            index = i + c*lseg
            result[c].append(listToCut[index])
    n=0
    for c in range(ncut-reste, ncut):
        result.append([])
        for i in range(lseg2):
            index2 = i + lseg * (ncut-reste) + n * lseg2
            result[c].append(listToCut[index2])
        n += 1

    return {'container': result, 'ncut': ncut}


def getAllattr(ob:object):
    dc = ob.__dict__
    att = []
    for d in dc:
        if d[:2] != "__":
            att.append(d)
    return att


def scanDir(path: str, fileExt: str = None):
    if fileExt is not None:
        ext = '*.'+ fileExt
        req = path + ext
        return glob.glob(req)
    else:
        return glob.glob('*.*')