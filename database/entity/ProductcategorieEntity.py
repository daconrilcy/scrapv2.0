import datetime
from database import Entity


# @ORM/EntityName=product_categorie
class ProductcategorieEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=nom
    # @ORM/Column(type=varchar,length=50,nullable=YES)
    # ###
    _nom: str = None

    def getId(self):
        return self._id

    def getNom(self):
        return self._nom

    def setNom(self, nom: str):
        self._nom = nom[0:50]
        return self
