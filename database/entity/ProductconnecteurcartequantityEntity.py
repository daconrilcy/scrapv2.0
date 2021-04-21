import datetime
from database import Entity


# @ORM/EntityName=product_connecteur_carte_quantity
class ProductconnecteurcartequantityEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=connecteur_id
    # @ORM/Column(type=int,key=MUL,nullable=NO)
    # ###
    _connecteurId: int = None

    # ###
    # @ORM/FieldName=quantity
    # @ORM/Column(type=int,nullable=NO)
    # ###
    _quantity: int = None

    def getId(self):
        return self._id

    def getConnecteurid(self):
        return self._connecteurId

    def setConnecteurid(self, connecteurId: int):
        self._connecteurId = connecteurId
        return self

    def getQuantity(self):
        return self._quantity

    def setQuantity(self, quantity: int):
        self._quantity = quantity
        return self
