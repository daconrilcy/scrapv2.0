from database.entity import *
from database.annotation import EntityAnnotation, convertFieldToAttribute
from database import Table, Entity
from database.ORM import ORM
import tools

import re


class DatabaseMigrations:
    _ORM: ORM = None

    def __init__(self, orm: ORM):
        self._ORM = orm

    def migrateAllFromMysql(self):
        self._ORM.replaceAllEntityFromMysql()

    def migrateOneEntityToMysql(self):
        pass

    def compareEntitiesToMysql(self):
        pass

    def updateFromEntityToMysql(self):
        pass


class EntityManager:
    _annotation: EntityAnnotation
    _table: Table = None
    _entity = None
    _pathEntity = "database/entity/"
    _tableName = None
    _request = ""
    _prevEntityClass = None
    _ORM: ORM = None
    _errors = []
    migrations: DatabaseMigrations = None

    def __init__(self):
        self._annotation = EntityAnnotation()
        self._ORM = ORM()
        self.migrations = DatabaseMigrations(orm=self._ORM)

    def persist(self, entity: Entity):
        if len(self._errors) == 0:
            if self._entity is not None:
                self._prevEntityClass = self._entity.getName()
            self._getTable(entity)
            self._prepareRequest()

    def flush(self):
        m = re.findall(";", self._request)
        result = []
        if len(m) > 1:
            for c in self._ORM.connection.cursor().execute(self._request, multi=True):
                result.append(self._ORM.connection.commit())
        else:
            self._ORM.connection.cursor().execute(self._request)
            result.append(self._ORM.connection.commit())

        return result

    def _getTable(self, entity: Entity):
        self._annotation.seakEntity(entity)
        self._table = self._annotation.getTable()
        self._tableName = self._table.name
        # on remplace l'entity passé par celle de l'annotation qui est enrichie (ajout de a liste des attributs)
        self._entity = self._annotation.getEntity()

    def getById(self, entity: Entity, idInTable: int):
        if entity is not None:
            self._getTable(entity)
        if idInTable is None:
            return None
        self._request = "SELECT * FROM " + self._table.name + " WHERE " \
                        + self._table.getPrimaryKey() + " = " + str(idInTable) + ";"
        return self._fetchOne()

    def getOneBy(self, requestChain: dict):
        if requestChain is None:
            return None

    def getAll(self, entity: Entity = None):
        if entity is not None:
            self._getTable(entity)
        self._request = 'SELECT * from ' + self._table.name + ";"

        return self._fetchAll()

    def getallBy(self, requestChain: list, entity: Entity = None):
        if entity is not None:
            self._getTable(entity)
        if requestChain is None:
            return None
        self._request = "SELECT * FROM " + self._table.name + " WHERE "
        for rc in requestChain:
            if isinstance(rc[1], list):
                self._request += '('
                fi = rc[0]
                for r in rc[1]:
                    self._request += fi + "="
                    if isinstance(r, str):
                        self._request += "'" + r + "'"
                    else:
                        self._request += str(r)
                    self._request += " OR "
                self._request = self._request[:-4] + ")"
            else:
                if isinstance(rc[1], str):
                    self._request += rc[0] + "='" + rc[1] + "'"
                else:
                    self._request += rc[0] + "=" + str(rc[1])
            self._request += " AND "
        self._request = self._request[:-5] + ";"
        print(self._request)
        return self._fetchAll()

    def _prepareRequest(self):
        request = ""
        if self._request != "":
            self._request += "\n"
        primKey = self._entity.getPrimaryKey()
        primKeyValue = self._entity.__getattribute__(primKey)
        if not tools.dataNotNull(primKeyValue):
            if self._prevEntityClass != self._entity.getName():
                self._request += "INSERT INTO " + self._table.name + " ("
                for a in range(len(self._entity.getAttributes())):
                    attT = self._table.fieldsName[a]
                    self._request += attT + ","
                self._request = self._request[:-1] + ") VALUES ("
            else:
                self._request = self._request[:-2] + ",\n("

            self._request += "NULL,"
            for a in range(len(self._entity.getAttributes())):
                attE = self._entity.getAttributes()[a]
                if attE != primKey:
                    ft = self._table.fieldsName[a]
                    val = self._entity.__getattribute__(attE)
                    if (val is not None) | self._table.fields[ft].nullable:
                        if isinstance(val, str):
                            self._request += "'" + self._entity.__getattribute__(attE) + "',"
                        elif val is None:
                            self._request += "NULL,"
                        else:
                            self._request += str(self._entity.__getattribute__(attE)) + ","
                    else:
                        tools.addMessage("Erreur : le champ" + attE + "ne peut pas être null")
                        self._errors.append(attE)
                        self._request = ""
            if len(self._errors) == 0:
                self._request = self._request[:-1] + ");"

    def _fetchOne(self):
        cursor = self._ORM.connection.cursor()
        cursor.execute(self._request)
        return self._transformRequestResultInEntity(cursor.fetchone())

    def _fetchAll(self):
        cursor = self._ORM.connection.cursor()
        cursor.execute(self._request)
        result = cursor.fetchall()
        entities: list = []
        for r in result:
            entities.append(self._transformRequestResultInEntity(r))
        return entities

    def _transformRequestResultInEntity(self, result):
        rs = self._tableDescription()
        entity = self._entity.__class__()
        entity.clearAttibutes()
        for att in self._entity.getAttributes():
            entity.addAttributeToListAttributes(att)
        for i in range(len(result)):
            attr = entity.getAttributes()[i]
            entity.__setattr__(attr, result[i])

        return entity

    def _tableDescription(self):
        request = "DESCRIBE " + self._table.name + ";"
        cursor = self._ORM.connection.cursor()
        cursor.execute(request)
        return cursor.fetchall()



def defineTableNameFromEntityName(entityName: str):
    tableName = re.sub('Entity$', '', entityName)
    tableName = transformUpperTo_lower(tableName)
    return tableName


def transformUpperTo_lower(st: str):
    vs = re.findall('[A-Z]', st)
    for v in vs:
        r = re.search(v, st)
        if r.span()[0] != 0:
            rep = '_' + v.lower()
            b = re.sub(v, rep, st)
    return st.lower()
