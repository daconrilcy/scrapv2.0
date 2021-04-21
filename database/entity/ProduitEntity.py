import datetime
from database import Entity


# @ORM/EntityName=produit
class ProduitEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=designation
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _designation: str = None

    # ###
    # @ORM/FieldName=code_interne
    # @ORM/Column(type=varchar,length=20,nullable=NO)
    # ###
    _codeInterne: str = None

    # ###
    # @ORM/FieldName=reference
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _reference: str = None

    # ###
    # @ORM/FieldName=usn
    # @ORM/Column(type=varchar,length=50,nullable=NO)
    # ###
    _usn: str = None

    def getId(self):
        return self._id

    def getDesignation(self):
        return self._designation

    def setDesignation(self, designation: str):
        self._designation = designation[0:50]
        return self

    def getCodeinterne(self):
        return self._codeInterne

    def setCodeinterne(self, codeInterne: str):
        self._codeInterne = codeInterne[0:20]
        return self

    def getReference(self):
        return self._reference

    def setReference(self, reference: str):
        self._reference = reference[0:50]
        return self

    def getUsn(self):
        return self._usn

    def setUsn(self, usn: str):
        self._usn = usn[0:50]
        return self
