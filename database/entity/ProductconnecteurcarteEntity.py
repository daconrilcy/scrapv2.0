import datetime
from database import Entity


# @ORM/EntityName=product_connecteur_carte
class ProductconnecteurcarteEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=size_id
    # @ORM/Column(type=int,key=MUL,nullable=YES)
    # ###
    _sizeId: int = None

    # ###
    # @ORM/FieldName=nom
    # @ORM/Column(type=varchar,length=20,nullable=NO)
    # ###
    _nom: str = None

    # ###
    # @ORM/FieldName=version
    # @ORM/Column(type=varchar,length=20,nullable=YES)
    # ###
    _version: str = None

    # ###
    # @ORM/FieldName=bande_passante
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _bandePassante: int = None

    def getId(self):
        return self._id

    def getSizeid(self):
        return self._sizeId

    def setSizeid(self, sizeId: int):
        self._sizeId = sizeId
        return self

    def getNom(self):
        return self._nom

    def setNom(self, nom: str):
        self._nom = nom[0:20]
        return self

    def getVersion(self):
        return self._version

    def setVersion(self, version: str):
        self._version = version[0:20]
        return self

    def getBandepassante(self):
        return self._bandePassante

    def setBandepassante(self, bandePassante: int):
        self._bandePassante = bandePassante
        return self
