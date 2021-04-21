import re
import tools
from database import Table, FieldTable, findTypeFromMysql, Entity

baseCommandeAnnotation = ['EntityName', 'FieldName', 'Column', 'GeneratedValue']

startAnnotationFormat = "# ###"
shortComment = "# "
appelFonction = "@ORM/"
callage1 = "    "
callage2 = callage1 + callage1
callage3 = callage2 + callage1


def makeEnteteGetterSetter(field: FieldTable, typeDef: str = 'get'):
    st = 'def '
    typeDef = typeDef.lower()
    st += typeDef + convertNameToObjName(field.name).capitalize()
    if typeDef.lower() == 'set':
        st += '(self, ' + convertNameToObjName(field.name) + ': ' + field.type.python + '):\n'
    else:
        st += '(self):\n'

    return st


class CommandColumnAnnotation:
    type = "type"
    length = "length"
    key = "key"
    nullable = "nullable"
    appelFonction = shortComment + appelFonction + "Column"

    def createStringFromField(self, field: FieldTable):
        st = self.appelFonction + "("
        st += self._makePatternCommand(self.type, field.type.mysql)
        if field.length != 0:
            st += self._makePatternCommand(self.length, field.length)
        if field.key != '':
            st += self._makePatternCommand(self.key, field.key)
        if field.nullable:
            st += self._makePatternCommand(self.nullable, "YES")
        else:
            st += self._makePatternCommand(self.nullable, "NO")

        return st[:-1] + ')'

    def _makePatternCommand(self, fieldName, fieldValue):
        return fieldName + "=" + str(fieldValue) + ','


class FileCommentedCreator:
    _table: Table = None
    _filePath: str = None

    def __init__(self, table: Table = None, filePath: str = None):
        if table is not None:
            self._table = table
        if filePath is not None:
            self._filePath = filePath

    def _addAttributeFromTableFied(self):
        cA = CommandColumnAnnotation()
        st = ""
        for fn in self._table.fieldsName:
            field: FieldTable = self._table.fields[fn]
            debutLigne = callage1 + shortComment + appelFonction
            st += callage1 + startAnnotationFormat + '\n'
            st += debutLigne + baseCommandeAnnotation[1] + '=' + field.name + '\n'
            st += callage1 + cA.createStringFromField(field) + '\n'
            if field.extra:
                if field.extra == 'auto_increment':
                    st += debutLigne + baseCommandeAnnotation[3] + '\n'
            st += callage1 + startAnnotationFormat + '\n'
            st += callage1 + convertFieldToAttribute(field) + ": " + field.type.python
            st += " = None"
            st += "\n\n"
        return st

    def _addSetterGetter(self):
        st = ""
        for fn in self._table.fieldsName:
            field: FieldTable = self._table.fields[fn]
            st += callage1 + makeEnteteGetterSetter(field, 'get')
            st += callage2 + 'return self.' + convertFieldToAttribute(field) + '\n\n'
            if field.key != 'PRI':
                st += callage1 + makeEnteteGetterSetter(field, 'set')
                st += callage2 + 'self.' + convertFieldToAttribute(field) + ' = ' + convertNameToObjName(
                    field.name)
                if field.length > 1:
                    st += '[0:' + str(field.length) + ']'
                st += '\n'
                st += callage2 + 'return self\n\n'
        return st

    def convertMysqlToEntityFile(self, tableToPut: Table):
        if tableToPut is not None:
            self._table = tableToPut
        if self._table is None:
            return False
        st = 'import datetime\nfrom database import Entity\n\n\n'
        nameEntity = convertNameToObjName(self._table.name).capitalize()+"Entity"
        st += shortComment + appelFonction + baseCommandeAnnotation[0] + "=" + self._table.name + "\n"
        st += "class " + nameEntity + "(Entity):\n"

        st += self._addAttributeFromTableFied()
        st += self._addSetterGetter()

        st = st[:-1]

        if tools.dataNotNull(self._filePath):
            filename = self._filePath + nameEntity + '.py'
            fileW = open(filename, 'w')
            fileW.write(st)
            fileW.close()

            filePacketEntityPath = self._filePath + "__init__.py"
            with open(filePacketEntityPath, "a") as fileAd:
                st = "from database.entity." + nameEntity + " import " + nameEntity + "\n"
                fileAd.write(st)
                fileAd.close()
        return st


class EntityAnnotation:
    _entity: Entity = None
    _pathEntity = 'database/entity/'
    _lines = []
    _tableEncours: Table = None
    _fieldEncours: FieldTable = None
    _actualLine: str = None
    _entitesALreadyFormated = {}
    _tablesAlreadyDone = {}
    _nameMysqlFieldEncours = ""
    _fileCreator = FileCommentedCreator(filePath=_pathEntity)

    def __init__(self, entity: Entity = None, forceUpdate: bool = False):
        if entity is not None:
            self.seakEntity(entity, forceUpdate)

    def seakEntity(self, entity: Entity, forceUpdate: bool = False):
        if (entity.getName() not in self._entitesALreadyFormated.keys()) | forceUpdate:
            self._entity = entity
            self._tableEncours = Table()
            self._recupDatas()
            self._decoupeComment()
            self._entitesALreadyFormated[entity.getName()] = self._entity
            self._tablesAlreadyDone[entity.getName()] = self._tableEncours
        else:
            self._entity = self._entitesALreadyFormated[entity.getName()]
            self._tableEncours = self._tablesAlreadyDone[entity.getName()]
            self._recupDataWithCopieEntity(entity)

    def writeTableInEntityFile(self, table: Table = None):
        if table is not None:
            self._tableEncours = table
        self._fileCreator.convertMysqlToEntityFile(tableToPut=self._tableEncours)

    def _recupDatas(self):
        fileName = self._pathEntity + self._entity.getName() + '.py'
        with open(fileName, "r") as fopen:
            self._lines = fopen.readlines()

    def _decoupeComment(self):
        lfichier = len(self._lines)
        ln = 0
        commentStarted = False
        findEntity = "# @ORM/" + baseCommandeAnnotation[0] + "="
        self._entity.clearAttibutes()
        while ln < lfichier:
            self._actualLine = self._lines[ln]
            if self._fieldEncours:
                if preFormatLineAnnotation(self._actualLine)[0:1] == '_':
                    vals = preFormatLineAnnotation(self._actualLine)[1:].split(":")
                    self._entity.addAttributeToListAttributes(vals[0])
                    if self._fieldEncours.key == "PRI":
                        self._entity.setPrimaryKey(vals[0])
                        self._tableEncours.setPrimaryKey(self._nameMysqlFieldEncours)
            if self.isLineContain(stToContain=findEntity, addPreCarShort=False):
                self._tableEncours = Table()
                self._tableEncours.fieldsName = []
                self._tableEncours.name = preFormatLineAnnotation(self._actualLine)[18:]
            if self.isLineContain(startAnnotationFormat, False):
                commentStarted = True
                self._fieldEncours = FieldTable()
                ln += 1
                self._actualLine = self._lines[ln]
            if commentStarted:
                while not self.isLineContain(startAnnotationFormat, False):
                    self._actualLine = self._lines[ln]
                    if self.isLineContain("# @ORM/", False):
                        self._commandAnnotationEntity()
                    ln += 1
                    self._actualLine = self._lines[ln]
                self._tableEncours.fields[self._fieldEncours.name] = self._fieldEncours
                self._tableEncours.fieldsName.append(self._fieldEncours.name)
                commentStarted = False
            ln += 1

    def _commandAnnotationEntity(self):
        if not tools.dataNotNull(self._actualLine):
            return False
        marqueur = "@ORM/"
        clfM = len(marqueur) + 2
        if self.isLineContain("@ORM/", True):
            val = preFormatLineAnnotation(self._actualLine)[clfM:]
            lbca = len(baseCommandeAnnotation[1])
            com = val[0:lbca]
            if com == baseCommandeAnnotation[1]:
                self._fieldEncours = FieldTable()
                stName = lbca + 1
                self._fieldEncours.name = val[stName:]
                self._nameMysqlFieldEncours = val[stName:]
                return True
            lbca = len(baseCommandeAnnotation[2])
            com = val[0:lbca]
            if com == baseCommandeAnnotation[2]:
                self._commandeColumn(val)
                return True
            lbca = len(baseCommandeAnnotation[3])
            com = val[0:lbca]
            if com == baseCommandeAnnotation[3]:
                self._fieldEncours.extra = 'auto_increment'
                return True
        else:
            return False

    def _commandeColumn(self, line: str):
        # Commands => 'type', 'nullable', key
        cl = len(baseCommandeAnnotation[2]) + 1
        localCommandsSt = re.sub('\n', '', line[cl:])
        localCommandsSt = re.sub('\)$', '', localCommandsSt)
        localCommandsAr = localCommandsSt.split(",")
        for lc in localCommandsAr:
            lcNet = re.sub('^\s', '', lc)
            lcNet = re.sub('\s$', '', lcNet)
            if lcNet[0:4] == 'type':
                typeLine = re.sub("\(\d*\)", '', lcNet[5:])
                lenRech = re.search('\d+', lcNet[5:])
                if lenRech:
                    if lenRech.group(0):
                        self._fieldEncours.length = int(lenRech.group(0))
                    else:
                        self._fieldEncours.length = 0
                else:
                    self._fieldEncours.length = 0
                self._fieldEncours.type = findTypeFromMysql(typeLine)
            elif lcNet[0:3] == 'key':
                value = re.sub('^\s*', '', lcNet[4:])
                value = re.sub('\s=$', '', value)
                self._fieldEncours.key = value
            elif lcNet[0:8] == 'nullable':
                self._fieldEncours.nullable = True

        return

    def isLineContain(self, stToContain: str, addPreCarShort: bool = False):
        if addPreCarShort:
            stToContain = "# " + stToContain
        ltofind = len(stToContain)
        if preFormatLineAnnotation(self._actualLine)[0:ltofind] == stToContain:
            return True
        return False

    def getTable(self):
        return self._tableEncours

    def getEntity(self):
        return self._entity

    def _recupDataWithCopieEntity(self, newEntity: Entity):
        for attr in self._entity.getAttributes():
            self._entity.__setattr__(attr, newEntity.__getattribute__(attr))
            newEntity.addAttributeToListAttributes(attr)


def convertFieldToAttribute(field: FieldTable):
    return "_" + convertNameToObjName(field.name)


def convertAttibuteToField(attribute: str):
    if attribute[0:1] == "_":
        attribute = attribute[1:]
    captitals = re.findall('[A-Z]', attribute)
    for c in captitals:
        rep = "_" + c.lower()
        attribute = re.sub(c, rep, attribute)

    return attribute


def preFormatLineAnnotation(line: str):
    line = re.sub('^\s*', "", line)
    line = re.sub('\n', "", line)
    return line


def convertNameToObjName(name: str = None):
    if name is None:
        return ""
    ln = len(name)
    returnedName: str = ""
    nextUpper = False
    for i in range(ln):
        if nextUpper:
            returnedName += name[i:i + 1].upper()
            nextUpper = False
        else:
            if name[i:i + 1] == "_":
                nextUpper = True
            else:
                nextUpper = False
                returnedName += name[i:i + 1].lower()
    return returnedName
