import datetime
from database import Entity


# @ORM/EntityName=memory_ss_type
class MemorysstypeEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=type_id
    # @ORM/Column(type=int,key=MUL,nullable=NO)
    # ###
    _typeId: int = None

    # ###
    # @ORM/FieldName=name
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _name: str = None

    # ###
    # @ORM/FieldName=memory_base_clock
    # @ORM/Column(type=int,nullable=NO)
    # ###
    _memoryBaseClock: int = None

    def getId(self):
        return self._id

    def getTypeid(self):
        return self._typeId

    def setTypeid(self, typeId: int):
        self._typeId = typeId
        return self

    def getName(self):
        return self._name

    def setName(self, name: str):
        self._name = name[0:50]
        return self

    def getMemorybaseclock(self):
        return self._memoryBaseClock

    def setMemorybaseclock(self, memoryBaseClock: int):
        self._memoryBaseClock = memoryBaseClock
        return self
