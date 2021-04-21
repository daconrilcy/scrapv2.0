import datetime
from database import Entity


# @ORM/EntityName=gpu
class GpuEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=brand_id
    # @ORM/Column(type=int,key=MUL,nullable=NO)
    # ###
    _brandId: int = None

    # ###
    # @ORM/FieldName=nom
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _nom: str = None

    # ###
    # @ORM/FieldName=core_frequency
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _coreFrequency: int = None

    # ###
    # @ORM/FieldName=memory
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _memory: int = None

    # ###
    # @ORM/FieldName=gravure
    # @ORM/Column(type=double,nullable=YES)
    # ###
    _gravure: float = None

    # ###
    # @ORM/FieldName=gamme
    # @ORM/Column(type=varchar,length=20,nullable=YES)
    # ###
    _gamme: str = None

    # ###
    # @ORM/FieldName=generation_name
    # @ORM/Column(type=varchar,length=50,nullable=YES)
    # ###
    _generationName: str = None

    def getId(self):
        return self._id

    def getBrandid(self):
        return self._brandId

    def setBrandid(self, brandId: int):
        self._brandId = brandId
        return self

    def getNom(self):
        return self._nom

    def setNom(self, nom: str):
        self._nom = nom[0:50]
        return self

    def getCorefrequency(self):
        return self._coreFrequency

    def setCorefrequency(self, coreFrequency: int):
        self._coreFrequency = coreFrequency
        return self

    def getMemory(self):
        return self._memory

    def setMemory(self, memory: int):
        self._memory = memory
        return self

    def getGravure(self):
        return self._gravure

    def setGravure(self, gravure: float):
        self._gravure = gravure
        return self

    def getGamme(self):
        return self._gamme

    def setGamme(self, gamme: str):
        self._gamme = gamme[0:20]
        return self

    def getGenerationname(self):
        return self._generationName

    def setGenerationname(self, generationName: str):
        self._generationName = generationName[0:50]
        return self
