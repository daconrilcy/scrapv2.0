import datetime
from database import Entity


# @ORM/EntityName=product_accesories
class ProductaccesoriesEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=description
    # @ORM/Column(type=varchar,length=100,nullable=NO)
    # ###
    _description: str = None

    def getId(self):
        return self._id

    def getDescription(self):
        return self._description

    def setDescription(self, description: str):
        self._description = description[0:100]
        return self
