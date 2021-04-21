import datetime
from database import Entity


# @ORM/EntityName=product_connecteur_alim
class ProductconnecteuralimEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=description
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _description: str = None

    def getId(self):
        return self._id

    def getDescription(self):
        return self._description

    def setDescription(self, description: str):
        self._description = description[0:50]
        return self
