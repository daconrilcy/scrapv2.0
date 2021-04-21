import datetime
from database import Entity


# @ORM/EntityName=brand
class BrandEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=nom
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _nom: str = None

    # ###
    # @ORM/FieldName=siteweb
    # @ORM/Column(type=varchar,length=100,nullable=YES)
    # ###
    _siteweb: str = None

    def getId(self):
        return self._id

    def getNom(self):
        return self._nom

    def setNom(self, nom: str):
        self._nom = nom[0:50]
        return self

    def getSiteweb(self):
        return self._siteweb

    def setSiteweb(self, siteweb: str):
        self._siteweb = siteweb[0:100]
        return self
