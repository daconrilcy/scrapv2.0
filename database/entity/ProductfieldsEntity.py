import datetime
from database import Entity


# @ORM/EntityName=product_fields
class ProductfieldsEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=gpu_id
    # @ORM/Column(type=int,key=MUL,nullable=YES)
    # ###
    _gpuId: int = None

    # ###
    # @ORM/FieldName=memory_id
    # @ORM/Column(type=int,key=MUL,nullable=YES)
    # ###
    _memoryId: int = None

    # ###
    # @ORM/FieldName=size_id
    # @ORM/Column(type=int,key=MUL,nullable=YES)
    # ###
    _sizeId: int = None

    # ###
    # @ORM/FieldName=cooling_id
    # @ORM/Column(type=int,key=MUL,nullable=YES)
    # ###
    _coolingId: int = None

    # ###
    # @ORM/FieldName=psu
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _psu: int = None

    # ###
    # @ORM/FieldName=conso_max
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _consoMax: int = None

    # ###
    # @ORM/FieldName=conso_moy
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _consoMoy: int = None

    # ###
    # @ORM/FieldName=nombre_ecran
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _nombreEcran: int = None

    # ###
    # @ORM/FieldName=date_lancement
    # @ORM/Column(type=date,nullable=YES)
    # ###
    _dateLancement: datetime.date = None

    # ###
    # @ORM/FieldName=datefin
    # @ORM/Column(type=date,nullable=YES)
    # ###
    _datefin: datetime.date = None

    # ###
    # @ORM/FieldName=led
    # @ORM/Column(type=tinyint,length=1,nullable=YES)
    # ###
    _led: bool = None

    def getId(self):
        return self._id

    def getGpuid(self):
        return self._gpuId

    def setGpuid(self, gpuId: int):
        self._gpuId = gpuId
        return self

    def getMemoryid(self):
        return self._memoryId

    def setMemoryid(self, memoryId: int):
        self._memoryId = memoryId
        return self

    def getSizeid(self):
        return self._sizeId

    def setSizeid(self, sizeId: int):
        self._sizeId = sizeId
        return self

    def getCoolingid(self):
        return self._coolingId

    def setCoolingid(self, coolingId: int):
        self._coolingId = coolingId
        return self

    def getPsu(self):
        return self._psu

    def setPsu(self, psu: int):
        self._psu = psu
        return self

    def getConsomax(self):
        return self._consoMax

    def setConsomax(self, consoMax: int):
        self._consoMax = consoMax
        return self

    def getConsomoy(self):
        return self._consoMoy

    def setConsomoy(self, consoMoy: int):
        self._consoMoy = consoMoy
        return self

    def getNombreecran(self):
        return self._nombreEcran

    def setNombreecran(self, nombreEcran: int):
        self._nombreEcran = nombreEcran
        return self

    def getDatelancement(self):
        return self._dateLancement

    def setDatelancement(self, dateLancement: datetime.date):
        self._dateLancement = dateLancement
        return self

    def getDatefin(self):
        return self._datefin

    def setDatefin(self, datefin: datetime.date):
        self._datefin = datefin
        return self

    def getLed(self):
        return self._led

    def setLed(self, led: bool):
        self._led = led
        return self
