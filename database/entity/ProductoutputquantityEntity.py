import datetime
from database import Entity


# @ORM/EntityName=product_output_quantity
class ProductoutputquantityEntity(Entity):
    # ###
    # @ORM/FieldName=id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # @ORM/GeneratedValue
    # ###
    _id: int = None

    # ###
    # @ORM/FieldName=output_id
    # @ORM/Column(type=int,key=MUL,nullable=NO)
    # ###
    _outputId: int = None

    # ###
    # @ORM/FieldName=quantity
    # @ORM/Column(type=int,nullable=NO)
    # ###
    _quantity: int = None

    def getId(self):
        return self._id

    def getOutputid(self):
        return self._outputId

    def setOutputid(self, outputId: int):
        self._outputId = outputId
        return self

    def getQuantity(self):
        return self._quantity

    def setQuantity(self, quantity: int):
        self._quantity = quantity
        return self
