import datetime
from database import Entity


# @ORM/EntityName=product_output
class ProductoutputEntity(Entity):
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

    # ###
    # @ORM/FieldName=version
    # @ORM/Column(type=varchar,length=10,nullable=YES)
    # ###
    _version: str = None

    def getId(self):
        return self._id

    def getDescription(self):
        return self._description

    def setDescription(self, description: str):
        self._description = description[0:100]
        return self

    def getVersion(self):
        return self._version

    def setVersion(self, version: str):
        self._version = version[0:10]
        return self
