import datetime
from database import Entity


# @ORM/EntityName=product_fields_product_connecteur_carte_quantity
class ProductfieldsproductconnecteurcartequantityEntity(Entity):
    # ###
    # @ORM/FieldName=product_fields_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productFieldsId: int = None

    # ###
    # @ORM/FieldName=product_connecteur_carte_quantity_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productConnecteurCarteQuantityId: int = None

    def getProductfieldsid(self):
        return self._productFieldsId

    def getProductconnecteurcartequantityid(self):
        return self._productConnecteurCarteQuantityId
