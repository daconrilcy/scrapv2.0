import datetime
from database import Entity


# @ORM/EntityName=product_fields_product_accesories
class ProductfieldsproductaccesoriesEntity(Entity):
    # ###
    # @ORM/FieldName=product_fields_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productFieldsId: int = None

    # ###
    # @ORM/FieldName=product_accesories_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productAccesoriesId: int = None

    def getProductfieldsid(self):
        return self._productFieldsId

    def getProductaccesoriesid(self):
        return self._productAccesoriesId
