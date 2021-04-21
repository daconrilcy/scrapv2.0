import datetime
from database import Entity


# @ORM/EntityName=product_memory
class ProductmemoryEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=sous_type_id
    # @ORM/Column(type=int,key=MUL,nullable=NO)
    # ###
    _sousTypeId: int = None

    # ###
    # @ORM/FieldName=specific_clock
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _specificClock: int = None

    # ###
    # @ORM/FieldName=size
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _size: int = None

    def getId(self):
        return self._id

    def getSoustypeid(self):
        return self._sousTypeId

    def setSoustypeid(self, sousTypeId: int):
        self._sousTypeId = sousTypeId
        return self

    def getSpecificclock(self):
        return self._specificClock

    def setSpecificclock(self, specificClock: int):
        self._specificClock = specificClock
        return self

    def getSize(self):
        return self._size

    def setSize(self, size: int):
        self._size = size
        return self
