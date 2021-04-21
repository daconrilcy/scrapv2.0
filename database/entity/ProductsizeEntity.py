import datetime
from database import Entity


# @ORM/EntityName=product_size
class ProductsizeEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=largeur
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _largeur: int = None

    # ###
    # @ORM/FieldName=longueur
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _longueur: int = None

    # ###
    # @ORM/FieldName=hauteur
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _hauteur: int = None

    # ###
    # @ORM/FieldName=slot_size
    # @ORM/Column(type=double,nullable=YES)
    # ###
    _slotSize: float = None

    # ###
    # @ORM/FieldName=factor_format
    # @ORM/Column(type=varchar,length=20,nullable=YES)
    # ###
    _factorFormat: str = None

    def getId(self):
        return self._id

    def getLargeur(self):
        return self._largeur

    def setLargeur(self, largeur: int):
        self._largeur = largeur
        return self

    def getLongueur(self):
        return self._longueur

    def setLongueur(self, longueur: int):
        self._longueur = longueur
        return self

    def getHauteur(self):
        return self._hauteur

    def setHauteur(self, hauteur: int):
        self._hauteur = hauteur
        return self

    def getSlotsize(self):
        return self._slotSize

    def setSlotsize(self, slotSize: float):
        self._slotSize = slotSize
        return self

    def getFactorformat(self):
        return self._factorFormat

    def setFactorformat(self, factorFormat: str):
        self._factorFormat = factorFormat[0:20]
        return self
