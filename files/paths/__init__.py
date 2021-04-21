from database.ORM import ORM

filesPath = "files/"


class DataBrutesFilesPath:
    localPath = "databrutes/"

    def __init__(self, brandPath: str):
        self.listeRefBrut = brandPath + self.localPath + "liste_ref_brut.txt"
        self.datasCaractProduct = brandPath + self.localPath + "listeProduitBrut.txt"


class DataCleanPath:
    localPath: str = "dataclean/"

    def __init__(self, brandPath: str):
        self.listesReferencesOrganisees = brandPath + self.localPath + "liste_ref_orga.txt"


class OtherFilePath:
    path = filesPath
    caterogieProduit = path + "product_categories.csv"
    marques = path + "brand.txt"
    fieldsAll = path + "official_field_list.csv"
    fieldsAbsent = path + "field_non_present.txt"


class BrandFilesPath:
    def __init__(self, brand: str):
        self.brand = brand
        self.brandPath: str = filesPath + brand + "/"
        self.databrutes: DataBrutesFilesPath = DataBrutesFilesPath(self.brandPath)
        self.dataclean: DataCleanPath = DataCleanPath(self.brandPath)
        self.fields: str = self.brandPath + "fields.txt"
        self.excludedfromExtract = self.brandPath + "data_not_extracted.txt"
        self.FieldsCorrespond = self.brandPath + "fields_correspond.txt"


class FilesNamesSarter:
    other = OtherFilePath()
    # Ajouter ici les files path par Marque, boutiques, etc.


def updateFilesBrand():
    # Creation des classes BrandFiles par Marque, creation de la classe Chapeau FileNames dans une string
    # que l'on enregistre dans un fichier py adéquate.

    # on recupère la liste de marque dans la base de données:
    orm = ORM()
    brands = []
    # Creation de la string avec toutes les classes brandFile par marque
    orm.request = "SELECT nom FROM brand;"
    requestResult = orm.fetchAll()
    for r in requestResult:
        brands.append(r[0])
    st = 'from files.paths import OtherFilePath\n'
    st += "from files.paths import BrandFilesPath\n\n"
    stFnO = "    other = OtherFilePath()\n"
    for b in brands:
        if b.lower() != "inconnu":
            BrandClass = b.capitalize()
            st += BrandClass + " = BrandFilesPath(brand='" + b + "')\n"
            stFnO += '    ' + BrandClass + ' = ' + BrandClass + '\n'
    # creation de l'objet chapeau contenant tous les objets de FilesBrand
    st += '\n\n'
    st += 'class FileNamesModel:\n' + stFnO
    st += "\n\nFilesNames = FileNamesModel()\n"

    # enregistrement dans le fichier adéquate
    pathclassPath = filesPath + "paths/pathclass.py"
    with open(pathclassPath, "w") as fpc:
        fpc.write(st)
        fpc.close()
