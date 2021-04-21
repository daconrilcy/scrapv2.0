from database.ORM import ORM
from files.paths.pathclass import FilesNames
import re


class CategorieProduitType:
    def __init__(self, index: int, description: str):
        self.index = index
        self.description = description


class _BrandsModel:
    def __init__(self, brands: list[str]):
        for b in brands:
            self.__setattr__(b, b)


class _CategoriesProduitModel:
    def __init__(self, categories: list[CategorieProduitType]):
        for c in categories:
            self.__setattr__(c.description, categories)


def _loadBrandList():
    with open(FilesNames.other.marques) as fb:
        lines = fb.readlines()
    for i in range(len(lines)):
        lines[i] = re.sub('\n', '', lines[i])
    return lines


def _loadCategoriesProduits():
    orm = ORM()
    request = 'SELECT * FROM product_categorie'
    cursor = orm.connection.cursor()
    cursor.execute(request)
    result = cursor.fetchall()
    cps = []
    for r in result:
        cps.append(CategorieProduitType(index=r[0], description=r[1]))
    return cps


BrandsObj = _BrandsModel(brands=_loadBrandList())
BrandList = _loadBrandList()
CategoriesProduits = _CategoriesProduitModel(categories=_loadCategoriesProduits())
