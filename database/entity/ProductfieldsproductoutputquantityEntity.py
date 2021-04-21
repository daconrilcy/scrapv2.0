import datetime
from database import Entity


# @ORM/EntityName=product_fields_product_output_quantity
class ProductfieldsproductoutputquantityEntity(Entity):
    # ###
    # @ORM/FieldName=product_fields_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productFieldsId: int = None

    # ###
    # @ORM/FieldName=product_output_quantity_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productOutputQuantityId: int = None

    def getProductfieldsid(self):
        return self._productFieldsId

    def getProductoutputquantityid(self):
        return self._productOutputQuantityId
