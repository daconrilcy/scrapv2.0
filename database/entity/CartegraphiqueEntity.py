import datetime
from database import Entity


# @ORM/EntityName=carte_graphique
class CartegraphiqueEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=boost_clock
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _boostClock: int = None

    # ###
    # @ORM/FieldName=memory_size
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _memorySize: int = None

    # ###
    # @ORM/FieldName=memory_clock
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _memoryClock: int = None

    # ###
    # @ORM/FieldName=lenght
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _lenght: int = None

    # ###
    # @ORM/FieldName=width
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _width: int = None

    # ###
    # @ORM/FieldName=height
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _height: int = None

    # ###
    # @ORM/FieldName=slot
    # @ORM/Column(type=double,nullable=YES)
    # ###
    _slot: float = None

    # ###
    # @ORM/FieldName=psu
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _psu: int = None

    # ###
    # @ORM/FieldName=output
    # @ORM/Column(type=varchar,length=100,nullable=YES)
    # ###
    _output: str = None

    def getId(self):
        return self._id

    def getBoostclock(self):
        return self._boostClock

    def setBoostclock(self, boostClock: int):
        self._boostClock = boostClock
        return self

    def getMemorysize(self):
        return self._memorySize

    def setMemorysize(self, memorySize: int):
        self._memorySize = memorySize
        return self

    def getMemoryclock(self):
        return self._memoryClock

    def setMemoryclock(self, memoryClock: int):
        self._memoryClock = memoryClock
        return self

    def getLenght(self):
        return self._lenght

    def setLenght(self, lenght: int):
        self._lenght = lenght
        return self

    def getWidth(self):
        return self._width

    def setWidth(self, width: int):
        self._width = width
        return self

    def getHeight(self):
        return self._height

    def setHeight(self, height: int):
        self._height = height
        return self

    def getSlot(self):
        return self._slot

    def setSlot(self, slot: float):
        self._slot = slot
        return self

    def getPsu(self):
        return self._psu

    def setPsu(self, psu: int):
        self._psu = psu
        return self

    def getOutput(self):
        return self._output

    def setOutput(self, output: str):
        self._output = output[0:100]
        return self
