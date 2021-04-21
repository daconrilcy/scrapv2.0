from files.paths.pathclass import FilesNames
from database.basics import BrandList, CategorieProduitType
from database.entityManager import EntityManager, Entity
from database.entity import CartegraphiqueEntity
import tools, re, json, os

_fileAbsName = "data.txt"
_fileFieldOfficielName = "data2.txt"


def loadFieldListeOfficial():
    em = EntityManager()
    CGs: list[CartegraphiqueEntity] = em.getAll(CartegraphiqueEntity())
    cg_Fields = []
    for c in CGs[0].getAttributes():
        if c != '_id':
            cg_Fields.append(c)
    return {'carte_graphique': cg_Fields}


_official_liste_cg = loadFieldListeOfficial()['carte_graphique']


def loadBrandFields(brand: str):
    if os.path.isfile(FilesNames.__getattribute__(brand).fields):
        with open(FilesNames.__getattribute__(brand).fields, "r") as ff:
            try:
                fields = json.load(ff)
                ff.close()
            except ValueError:
                return []
        return fields
    return []


def saveBrandFields(brand: str, fieldsList: list):
    with open(FilesNames.__getattribute__(brand).fields, "w") as ff:
        json.dump(fieldsList, ff)
        ff.close()


class FieldCorrespondPerBrand:
    def __init__(self, brandFieldName: str, officialFieldName: str):
        self.brandFieldName = brandFieldName
        self.officialName = officialFieldName


class FieldCorrespondAll:
    def __init__(self, name: str = None, categorie: CategorieProduitType = None):
        self.name: str = name
        self.categories: categorie
        self.brands = BrandList
        for b in BrandList:
            self.__setattr__(name=b, value="")


class FieldsOfficielsName:
    def __init__(self, listFiedOfficiels: list):
        self._attributes = []
        for fo in listFiedOfficiels:
            self.__setattr__(fo.name, fo)
            self._attributes.append(fo.name)

    def getAttibutes(self):
        return self._attributes


class ExempleData:
    founded = False
    productName = ""
    values = ""
    nFound = 0
    previousValue = ""


class FieldAbsent:
    brand = None
    fieldName = None
    exemple = None

    def __init__(self, brand: str, fieldName: str, exemple: [ExempleData] = None):
        self.brand = brand
        self.fieldName = fieldName
        self.exemple = exemple


def saveFileNonPresent(fieldsNonPresent: [FieldAbsent], raz: bool = False):
    brand = 'other'
    if tools.dataNotNull(fieldsNonPresent):
        brand = fieldsNonPresent[0].brand
    datasTopPut = []
    existingDatas = loadFileNonPresent()
    if not raz:
        if tools.dataNotNull(existingDatas[brand]):
            datasTopPut.extend(existingDatas[brand])
    for fa in fieldsNonPresent:
        objField = {"fieldName": fa.fieldName, 'exemple': []}
        if tools.dataNotNull(fa.exemple):
            for e in fa.exemple:
                objField['exemple'].append(e.values)
        datasTopPut.append(objField)

    existingDatas[brand] = datasTopPut

    with open(_fileAbsName, 'w') as outfile:
        json.dump(existingDatas, outfile)


def clearFileNonPresent():
    with open(FilesNames.other.marques, "r") as fo:
        brands = fo.readlines()
        for i in range(len(brands)):
            brands[i] = re.sub('\n', '', brands[i])

    datas = {}
    with open(_fileAbsName, "w") as fa:
        for b in brands:
            datas[b] = []
        json.dump(datas, fa)
        fa.close()


def clearABrandDateInFileNonePresent(brand: str):
    datas = loadFileNonPresent()
    if brand in datas.keys():
        datas[brand] = []
        with open(_fileAbsName, "w") as faf:
            json.dump(datas, faf)
            faf.close()
    else:
        clearFileNonPresent()


def loadFileNonPresent(brand: str = None):
    try:
        with open(_fileAbsName, "r") as faf:
            jsonDatas = json.load(faf, )
            faf.close()
        a = jsonDatas
        if jsonDatas:
            if brand:
                if brand in jsonDatas.keys():
                    return jsonDatas[brand]
            else:
                return jsonDatas
    except ValueError:
        return {}
    return {}


def LoadCorrespondOfficialListBrand(brand: str):
    pass


def checkFieldsList(brand: str, fields: list):
    pass


"""
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
"""
