import datetime
from database import Entity


# @ORM/EntityName=product_cooling
class ProductcoolingEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=name
    # @ORM/Column(type=varchar,length=20,nullable=NO)
    # ###
    _name: str = None

    # ###
    # @ORM/FieldName=desciption
    # @ORM/Column(type=varchar,length=255,nullable=YES)
    # ###
    _desciption: str = None

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name: str):
        self._name = name[0:20]
        return self

    def getDesciption(self):
        return self._desciption

    def setDesciption(self, desciption: str):
        self._desciption = desciption[0:255]
        return self
