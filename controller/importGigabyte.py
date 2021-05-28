import requests
from tools import *
from files import ActionFile, ExempleData
import json


class ImageLink:
    def __init__(self, name: str, fileFormat: str, link: str, title: str):
        self.name = name
        self.fileFormat = fileFormat
        self.link = link
        self.title = title


class CaractProduitBrute:
    def __init__(self, dataBrute):
        self.id = dataBrute['MainProductId']
        self.map = dataBrute['ProductSpecItem']
        self.spec = dataBrute['ProductSpecList']


class ObjClean:
    def __init__(self, idProduct: str, nom: str, productCode: str,
                 description: str, imagelist: list, version: str, lien: str, cat: str):
        self.idProduct = idProduct
        self.productCode = productCode
        self.nom = nom
        self.description = description
        self.imageList = imagelist
        self.version = version
        self.link = lien
        self.categorie = cat


class ImportGigabyte:
    """
     le site gigabyte est un site utilisant angular. Donc pas de scrapping HTML (tout est en requete AJAX/Javascript)
     La bonne nouvelle c'est que le site va chercher ses infos avec des requetes ajax que l'on peut recuperer
     avec les outils de Firefox (HTTP Header Spy) et les tester avec l'outil chrome servistate HTTP editor & Rest API
     Du coup, la recupération de données est simplifié : requete API qui renvoie des datas en format JSON
     """

    dataFile = None
    param_cat = None
    source = None
    liste_ref = []
    fields_Origin = []
    caract_produits = []
    excluded = []
    brand = "Gigabyte"
    filesGigabyte = None

    dataProductBrutes = []

    nRequetesMax = 15
    testMaxNumber = 300

    baseurl = "https://www.gigabyte.com/"
    url1 = "https://www.gigabyte.com/Ajax/Product/GetListInfoByAjax"
    url2 = "https://www.gigabyte.com/api/ProductSpec/"

    exceptions = ['5928', '5929', '5930',
                  '6041', '6056', '6058',
                  '6183', '6184',
                  '6238', '6239', '6290', '6291',
                  '6317', '6319', '6320',
                  '6446',
                  '6553', '6568', '6569', '6570', '6571', '6572', '6573', '6575', '6576',
                  '6727', '6728',
                  '6808',
                  '7581',
                  '7661', '7662',
                  '7064',
                  ]

    def __init__(self):
        self.dataFile = ActionFile()
        self.param_cat = "3"
        self.filesGigabyte = self.dataFile.fileNames.Gigabyte
        self.fields_pre_List = []
        self.liste_ref_brutes = None

    # Fonctions principales
    def importDatas(self, source: str = "web"):
        importer(source, self._getlist_productfromWeb, self._getlist_productfromFile)
        importer(source, self._recupAllProductfromWeb, self._recupAllProductfromFile)

    def traitements(self):
        self._traitementFieldsinDataBrute()

    # sous fonctions
    def _getlist_productfromFile(self):
        self.liste_ref = self.dataFile.loadDataBruteJsonToFile(
            self.dataFile.fileNames.gigabyte.databrutes.listeRefOrga)

    def _getlist_productfromWeb(self):
        addMessage("Recherches des références")
        # Obtenir la liste des cartes graphiques - pour cela il faut lister les pages de la categorie, recuperer les
        # references des cartes pour les réutiliser dans la requete des specificités produits

        totalpage = self._findTotalPage()
        addMessage("Extraction des références")
        argus = varToArg(totalpage + 1, "n")
        segPage = cutListInN(argus, self.nRequetesMax)

        self.liste_ref_brutes = threader(nThread=segPage['ncut'], function=self._recupDataPage,
                                         args=segPage['container'], messageIntermediare=True, addedText="pages listées")

        self._DataPageBruteToClear()

        self.dataFile.saveDataBruteJsonToFile(self.filesGigabyte.databrutes.listeRefBrut, self.liste_ref_brutes)
        self.dataFile.saveDataBruteJsonToFile(self.filesGigabyte.dataclean.listesReferencesOrganisees, self.liste_ref)

    def _findTotalPage(self):
        # recuperation de la page 1 et du nombre de pages :
        prm = "ck=" + self.param_cat + "&f=&page=1"
        reponse = requests.post(self.url1, params=prm).json()
        totalpage = int(reponse['MaximumPage'])
        addMessage(str(totalpage) + " pages à scruter")
        return totalpage

    def _recupDataPage(self, seqPages, container: list):
        # extraction des datas de chaque page de liste de ref
        for uPage in seqPages:
            if uPage['n'] != 0:
                page = uPage['n']
                prm = "ck=" + self.param_cat + "&f=&page=" + str(page)
                reponse = requests.post(self.url1, params=prm).json()
                container.append(reponse)

    def _DataPageBruteToClear(self):
        # epuration et organisation des liste de ref extraites.
        container = []
        excluded = []
        for data in self.liste_ref_brutes:
            for d in data['ModelList']:
                idreceived = str(d['MainInfo']['seq_product'])
                if not self._isIdInException(idreceived):
                    """
                    container.append(
                        {'id': idreceived,
                         "nomcomplet": d['LocalInfo']['name'],
                         "codeproduit": d['LocalInfo']['subtitle']
                         })
                    """
                    container.append(
                        ObjClean(idProduct=idreceived,
                                 nom=d['LocalInfo']['name'],
                                 productCode=d['MainInfo']['url_parame_name'],
                                 description=d['LocalInfo']['summary'],
                                 imagelist=self._getImageList(d['ImageList']),
                                 version=d['MainInfo']['version'],
                                 lien=self.baseurl + d['MainInfo']['UrlCountryCodeModel'],
                                 cat=d['MainInfo']['class_key']
                                 )
                    )
                else:
                    excluded.append({"brand": self.brand, "id": idreceived, "name": d['LocalInfo']['name']})
        self.liste_ref = container
        self.dataFile.savelistToFile(self.filesGigabyte.excludedfromExtract, excluded)
        addMessage(str(len(excluded)) + " données non extraites")

    def _recupAllProductfromWeb(self):
        addMessage("recuperation des caractéristiques produits")
        if len(self.liste_ref) > self.testMaxNumber:
            temp = self.liste_ref[:self.testMaxNumber]
            self.liste_ref = temp
        cutted = cutListInN(self.liste_ref, self.nRequetesMax)
        cutlist = cutted['container']
        nthread = cutted['ncut']
        self.dataProductBrutes = threader(nThread=nthread, function=self._threadrecupCaractProduit, args=cutlist,
                                          addedText=" produits avec details extraits", messageIntermediare=True)

        self.dataFile.saveDataBruteJsonToFile(
            fileName=self.dataFile.fileNames.Gigabyte.databrutes.datasCaractProduct,
            datas=self.dataProductBrutes)

    def _recupAllProductfromFile(self):
        self.dataProductBrutes = self.dataFile.loadDataBruteJsonToFile(
            self.filesGigabyte.databrutes.datasCaractProduct)

    def _threadrecupCaractProduit(self, listdatas, container: list):
        for datas in listdatas:
            if datas:
                #idRef = datas['id']
                idRef = datas.idProduct
                if idRef:
                    caract = self._recupCaractProduit(idRef)
                    if caract:
                        container.append(caract)

    def _recupCaractProduit(self, ref_produit: str):
        url = self.url2 + ref_produit
        rep = requests.get(url=url)

        if rep.status_code != 200:
            addMessage("Erreur recup " + ref_produit + " - errorCode :" + str(rep.status_code))
            return None
        else:
            try:
                a = rep.json()
            except ValueError:
                addMessage("Erreur creation Json " + ref_produit)
                a = None
            return a

    def _organizeDataProductBrute(self):
        self._traitementFieldsinDataBrute()

    # Gestion des champs
    def _traitementFieldsinDataBrute(self):
        self.fields_Origin = self._extractFieldNameinDataBrute()
        exempledatas = self._findExempleInDataProductField()
        self.dataFile.savelistToFile(
            fileName=self.filesGigabyte.fields,
            datas=self.fields_Origin)
        self.dataFile.checkFieldsList(self.brand, self.fields_Origin, exemplesData=exempledatas)

    def _extractFieldNameinDataBrute(self):
        fieldNames = []
        for data in self.dataProductBrutes:
            fields = data['map']
            for field in fields:
                fieldNames.append(field["Name"])
        return makeUnikList(fieldNames)

    def _findExempleInDataProductField(self):
        fieldsExemple = {}
        compteProd = {}
        compteExemple = {}
        lf = len(self.fields_Origin)
        for field in self.fields_Origin:
            fieldsExemple[field] = ExempleData()
            compteProd[field] = 0
            compteExemple[field] = 0
        nfound = 0
        for data in self.dataProductBrutes:
            caract = data['spec'][0]['ProductSpecData']
            for dc in caract:
                namField = dc['Name']
                fieldsExemple[namField].nFound += 1
                if not fieldsExemple[namField].founded:
                    if (fieldsExemple[namField].previousValue != str(dc['Description'])) & (
                            compteExemple[namField] <= 2):
                        fieldsExemple[namField].values += str(dc['Description']) + ","
                        fieldsExemple[namField].previousValue = dc['Description']
                        compteExemple[namField] += 1
                    if compteProd[namField] < 2:
                        fieldsExemple[namField].productName += str(data['spec'][0]['Name']) + ","
                        compteProd[namField] += 1
                    if (compteProd[namField] >= 2) & (compteExemple[namField] >= 2):
                        fieldsExemple[namField].founded = True
                        nfound += 1
                if nfound == lf:
                    break
            if nfound == lf:
                break

        for field in self.fields_Origin:
            if len(fieldsExemple[field].values) > 0:
                fieldsExemple[field].founded = True
                ex = str(fieldsExemple[field].values)
                dx = ex[0:-1]
                fieldsExemple[field].values = format(dx)
                fieldsExemple[field].productName = fieldsExemple[field].productName[0:-1]

        return fieldsExemple

    # Tools
    def _isIdInException(self, idReceived: str):
        return isInListe(idReceived, self.exceptions)

    def _getImageList(self, imageListBrut: list):
        result = []
        for iml in imageListBrut:
            url = self.baseurl + iml['ImageUrl']
            newIml = ImageLink(name=iml['name'], fileFormat=iml['ext'], title=iml['title'], link=url)
            result.append(newIml)

        return result


# tools dehors

class ObjJson:

    def __init__(self, objJson=None):
        self._initialObject = objJson
        self.type = None
        self.gotChilds = False
        self.nchilds = 0
        self.childs = None
        self.childsKeys = None
        self.keys = None

        self.putObj(objJson)
        self.findChilds()

    def putObj(self, obj):
        self._initialObject = obj
        if obj is not None:
            self.type = self._defType()
            self.gotChilds = self._isGotChilds()

    def _defType(self):
        if isinstance(self._initialObject, dict):
            return "dict"
        elif isinstance(self._initialObject, list):
            return "list"
        else:
            return "other"

    def _isGotChilds(self):

        if self.type == "dict":
            self.nchilds = len(self._initialObject.keys())

        elif self.type == "list":
            self.nchilds = len(self._initialObject)

        else:
            self.nchilds = 0

        if self.nchilds > 0:
            return True
        else:
            return False

    def findChilds(self):
        childs = None
        if self.gotChilds:
            childs = []
            self.childsKeys = []
            if self.type == "dict":
                self.keys = list(self._initialObject.keys())
                for k in self.keys:
                    childs.append(self._initialObject[k])
                    self.childsKeys.append({k: self._initialObject[k]})
            if self.type == "list":
                for c in self._initialObject:
                    childs.append(c)
                    if c:
                        self.childsKeys.append({"None": c})

        self.childs = childs

    def getForm(self):
        if self.type == "dict":
            return {}
        if self.type == "list":
            return []
        else:
            return None
