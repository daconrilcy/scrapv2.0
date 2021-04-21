import datetime
from database import Entity


# @ORM/EntityName=memory_type
class MemorytypeEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=name
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _name: str = None

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name: str):
        self._name = name[0:50]
        return self
