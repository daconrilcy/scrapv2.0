import re
import json
from tools import *
from files.paths.pathclass import FilesNames
from files.fields import FieldAbsent, ExempleData


class ActionFile:
    defaultPath = "files/"
    fileNames = None
    fields = None
    fieldsNonTrouves = None
    brands = None
    enteteFieds = ['official']

    def __init__(self):
        self._getFileName()
        self.brands = self.loadFileIntoList(filename=self.fileNames.other.marques)
        self.enteteFieds.extend(self.brands)
        self._importOfficialFieldListe()
        self.fieldsNonTrouves = self._loadFieldsNonTrouves()

    def _getFileName(self):
        self.fileNames = FilesNames

    def _importOfficialFieldListe(self):
        fields = self.loadFileIntoList(self.fileNames.other.fieldsAll)
        self.fields = []
        if len(fields) > 0:
            for field in fields:
                tmp = {}
                if field:
                    if len(field) == len(self.enteteFieds):
                        for i in range(len(field)):
                            tmp[self.enteteFieds[i]] = field[i]
                    else:
                        addMessage("taille des champs différents des entêtes")
                else:
                    addMessage("pas de donnees")
                    for i in range(len(self.enteteFieds)):
                        tmp[self.enteteFieds[i]] = ""
                self.fields.append(tmp)
        else:
            addMessage("Fichier des fields vide")

    def loadFileIntoList(self, filename):
        datas = []
        with open(filename, "r") as filout:
            lignes = filout.readlines()
            for ligne in lignes:
                tmp = ligne.split(",")
                if len(tmp) > 1:
                    val = []
                    for t in tmp:
                        val.append(re.sub("\n", "", t))
                    datas.append(val)
                elif len(tmp) == 1:
                    datas.append(re.sub("\n", "", tmp[0]))

        return datas

    def importBaseDataFromFile(self, sep: str = ";", sujet: str = "categorie produit"):
        if (sep is None) | (sep == ""):
            sep = ";"
        if (sujet is None) | (sujet == ""):
            sujet = "categories produit"
        path = self.findFileFromTitle(title=sujet)
        f = open(path, 'r')
        lignes = f.readlines()
        r = []
        for ligne in lignes:
            val = ligne.split(sep=sep)
            if len(val) > 0:
                if len(val) == 1:
                    v = re.sub("\n", "", val[0])
                    r.append(v)
                else:
                    r.append(val)
        return r

    def saveDataBruteJsonToFile(self, fileName: str, datas):
        if (fileName is None) | (fileName == '') | (datas is None):
            return False
        with open(fileName, "w") as fileout:
            json.dump(datas, fileout)
            fileout.close()

    def savelistToFile(self, fileName: str, datas: list):
        if (fileName is None) | (fileName == '') | (datas is None):
            return False
        toSave = ""
        for data in datas:
            strToRegister = ""
            if isinstance(data, dict):
                ks = data.keys()
                for k in ks:
                    strToRegister += str(data[k]) + ","
            elif isinstance(data, list):
                for d in data:
                    strToRegister += str(d) + ","
            elif isinstance(data, str):
                strToRegister = data + ","
            elif isinstance(data, (type, FieldAbsent)):
                keys = getAllattr(data)
                for k in keys:
                    if isinstance(data.__getattribute__(k), ExempleData):
                        strToRegister += re.sub(",", "/", data.__getattribute__(k).values) + ","
                    else:
                        strToRegister += str(data.__getattribute__(k)) + ","
            else:
                strToRegister = data + ","

            toSave += strToRegister[0:-1] + "\n"

        with open(fileName, "w") as fileout:
            fileout.write(format(json.dumps(toSave[0:-1])))

    def loadDataBruteJsonToFile(self, fileName: str):
        if (fileName is None) | (fileName == ''):
            return False
        with open(fileName, "r") as fileLoad:
            val = fileLoad.read()
            if val != '':
                return json.loads(val)
            else:
                return []

    def findFileFromTitle(self, title: str = "categorie produit"):
        title = title.lower()
        if re.search("(categorie)(s)?(\n)*(.)*", title):
            return self.fileNames.other.caterogieProduit
        if re.search("marque(s)?(\n)*(.)*", title):
            return self.fileNames.other.marques
        if re.search("brand(s)?(\n)*(.)*", title):
            return self.fileNames.other.marques

    def _loadFieldsNonTrouves(self):
        container = []
        f = open(self.fileNames.other.fieldsAbsent, "r")
        if f:
            lignes = f.readlines()
            if not dataNotNull(lignes):
                for ligne in lignes:
                    temp = ligne.split(",")
                    for i in range(2):
                        temp[i] = re.sub("\n", '', temp[i])
                    if temp:
                        container.append(FieldAbsent(brand=temp[0], fieldName=temp[1]))
            return container

    def checkFieldsList(self, brand: str, fieldsListe: list, exemplesData: dict):
        if not (dataNotNull(brand)) | (dataNotNull(fieldsListe)):
            return False
        fieldretened = []
        fieldNonPresents = []
        toAddOff = 0
        for ufn in fieldsListe:
            isIn = isInListeDetailled(data=ufn, listToCheck=self.fields)
            if isIn['result']:
                if self.fields[isIn['index']]['official'] != "":
                    fieldretened.append({"official": self.fields[isIn['index']]['official'], brand: ufn})
            else:
                tmp = {}
                for e in self.enteteFieds:
                    tmp[e] = ""
                    if e == brand:
                        tmp[e] = ufn
                self.fields.append(
                    tmp
                )
                toAddOff += 1
                fieldNonPresents.append(FieldAbsent(brand=brand, fieldName=ufn, exemple=exemplesData[ufn]))
                print("champ non présent:" + ufn)

        self.fieldsNonTrouves = fieldNonPresents
        addMessageN(len(fieldNonPresents), " fields non présents ajoutés")
        addMessage("sauvegarde des fields")
        self._saveListFieldOfficielle()
        self.savelistToFile(fileName=self.fileNames.other.fieldsAbsent, datas=self.fieldsNonTrouves)

    def _enregistrementFieldNonPresents(self, listfields: list):
        if not self.fieldsNonTrouves:
            self.fieldsNonTrouves = self._loadFieldsNonTrouves()
        add = 0
        if len(self.fieldsNonTrouves) > 0:
            for fi in listfields:
                toput = True
                for fn in self.fieldsNonTrouves:
                    if (fn.fieldName == fi.fieldName) & (fn.brand == fi.brand):
                        toput = False
                        break
                if toput:
                    self.fieldsNonTrouves.append(fi)
                    add += 1
        else:
            self.fieldsNonTrouves = listfields

        addMessageN(add, "nouveaux champs non trouvés additionnels")
        self.savelistToFile(fileName=self.fileNames.other.fieldsAbsent, datas=self.fieldsNonTrouves)

    def _saveListFieldOfficielle(self):
        if not dataNotNull(self.fields):
            addMessage("variable de la liste des fields est vide")
            return False
        stToFill = ""
        for field in self.fields:
            for e in self.enteteFieds:
                stToFill += field[e] + ","
            stToFill = stToFill[:-1] + "\n"

        with open(self.fileNames.other.fieldsAll, "w") as fileout:
            fileout.write(stToFill[0:-1])

