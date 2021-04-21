import re
import tools


class Entity:
    _attributes = []
    _name = ""
    _prim = None

    def __init__(self):
        self._name = self.__class__.__name__

    def getAttributes(self):
        return self._attributes

    def getName(self):
        return self._name

    def addAttributeToListAttributes(self, attributeName: str):
        if tools.dataNotNull(attributeName):
            if attributeName[0:1] != "_":
                attributeName = "_" + attributeName
            self._attributes.append(attributeName)

    def getPrimaryKey(self):
        return self._prim

    def setPrimaryKey(self, primaryKeyName: str):
        if primaryKeyName[0:1] != "_":
            primaryKeyName = "_"+primaryKeyName
        self._prim = primaryKeyName

    def clearAttibutes(self):
        self._attributes = []


class CorrTypeField:
    name = ""
    mysql = ""
    python = ""

    def __init__(self, mysqlValue: str = None, pythonValue: str = None):
        self.mysql = mysqlValue
        self.python = pythonValue


FieldTableTypes = {
    'string': CorrTypeField('varchar', 'str'),
    'varchar': CorrTypeField('varchar', 'str'),
    'str': CorrTypeField('varchar', 'str'),
    'int': CorrTypeField('int', "int"),
    'integer': CorrTypeField('int', "int"),
    'float': CorrTypeField('float', 'float'),
    'double': CorrTypeField('double', 'float'),
    'date': CorrTypeField('date', 'datetime.date'),
    'datetime': CorrTypeField('date', 'datetime.date'),
    'datetime.date': CorrTypeField('date', 'datetime.date'),
    'boolean': CorrTypeField('tinyint', 'bool'),
    'tinyint': CorrTypeField('tinyint', 'bool'),
    'bool': CorrTypeField('tinyint', 'bool'),
    'inconnu': CorrTypeField('', 'inconnu')
}


class FieldTable:
    name = ''
    type: CorrTypeField = None
    length = 0
    nullable: bool = False
    key = ''
    default = ''
    extra = ""
    filePath = "database/entity/"

    def __init__(self, name: str = None, typeField: CorrTypeField = None, length: int = 0):
        self.name = name
        self.type = typeField
        self.length = length


class Table:
    name = ""
    fieldsName = []
    attrName = []
    fields = {}
    _entity: Entity = None
    _primaryKey = None

    def __init__(self, name: str = None):
        self.name = name

    def getAttributes(self):
        if self._entity is not None:
            return self._entity.getAttributes()
        else:
            return None

    def getPrimaryKey(self):
        return self._primaryKey

    def setPrimaryKey(self, fieldPrimary: str):
        self._primaryKey = fieldPrimary


def formatTypeSizeFromBrutTableField(bruteType: str = None):
    lenVal = 0
    val = str(bruteType)
    val = re.sub('^b\'', '', val)
    val = re.sub('\'*', "", val)
    rechLen = re.search('\(\d*\)', val)
    if rechLen:
        if rechLen.group(0):
            val = re.sub('\(.*\)', '', val)
            lenVal = int(re.sub("[\(\)]", '', rechLen.group(0)))

    return {'type': val, 'len': lenVal}


def findTypeFromMysql(value):
    if value in FieldTableTypes:
        return FieldTableTypes[value]
    else:
        return CorrTypeField(value, 'inconnu')

