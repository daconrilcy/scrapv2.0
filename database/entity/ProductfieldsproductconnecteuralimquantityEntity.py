import datetime
from database import Entity


# @ORM/EntityName=product_fields_product_connecteur_alim_quantity
class ProductfieldsproductconnecteuralimquantityEntity(Entity):
    # ###
    # @ORM/FieldName=product_fields_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productFieldsId: int = None

    # ###
    # @ORM/FieldName=product_connecteur_alim_quantity_id
    # @ORM/Column(type=int,key=PRI,nullable=NO)
    # ###
    _productConnecteurAlimQuantityId: int = None

    def getProductfieldsid(self):
        return self._productFieldsId

    def getProductconnecteuralimquantityid(self):
        return self._productConnecteurAlimQuantityId
