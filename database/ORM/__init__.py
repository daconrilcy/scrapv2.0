from mysql.connector import connect, errors
import os
import tools
from context import Env
from database import Table, FieldTable, formatTypeSizeFromBrutTableField, findTypeFromMysql
from database.annotation import EntityAnnotation


def _importField(cursorAnswer: tuple = ()):
    field = FieldTable()
    if tuple != ():
        typeLen = formatTypeSizeFromBrutTableField(cursorAnswer[1])
        field.name = cursorAnswer[0]
        field.type = findTypeFromMysql(typeLen['type'])
        field.length = typeLen['len']
        if cursorAnswer[2] == "YES":
            field.nullable = True
        field.key = cursorAnswer[3]
        if cursorAnswer[4]:
            field.default = cursorAnswer[4]
        else:
            field.extra = ""
        if cursorAnswer[5]:
            field.extra = cursorAnswer[5]
        else:
            field.extra = ""
    return field


class ORM:
    connection = None
    cursor = None
    tablesNames = []
    tables = {}
    env = None
    filePath = "database/entity/"

    def __init__(self):
        self.env = Env()
        self._connectDatabase()
        self._getTables()
        self._getFieldsInTable()
        self.request = ""

    def _connectDatabase(self):
        if self.env is None:
            try:
                self.connection = connect(
                    host="192.168.1.46",
                    user="daconrilcy",
                    password="Cyrwebeur02",
                    database="spider2"
                )
                self.cursor = self.connection.cursor()
            except errors as e:
                print(e)
        else:
            try:
                self.connection = connect(
                    host=self.env.database.host,
                    user=self.env.database.user,
                    password=self.env.database.password,
                    database=self.env.database.database
                )
                self.cursor = self.connection.cursor()
            except errors as e:
                print(e)

    def _getTables(self):
        self.cursor.execute("SHOW TABLES")
        for c in self.cursor:
            self.tablesNames.append(c[0])
            self.tables[c[0]] = Table(name=c[0])

    def _getFieldsInTable(self):
        for table in self.tablesNames:
            self.tables[table].fieldsName = []
            self.tables[table].fields = {}
            self.cursor = self.connection.cursor()
            self.cursor.execute("DESCRIBE " + table)
            for c in self.cursor:
                field = _importField(c)
                self.tables[table].fieldsName.append(field.name)
                self.tables[table].fields[field.name] = field
            self.cursor = None

    def replaceAllEntityFromMysql(self):
        self._supprFileEntity()
        annot = EntityAnnotation()
        for tableName in self.tablesNames:
            annot.writeTableInEntityFile(self.tables[tableName])

    def _supprFileEntity(self):
        filesNames = tools.scanDir("database/entity/", "py")
        for f in filesNames:
            if f != '__init__.py':
                fname = f
                os.remove(fname)
        with open('__init__.py', "w") as fw:
            fw.write("")
            fw.close()

    def fetchAll(self):
        if tools.dataNotNull(self.request):
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.request)
            return self.cursor.fetchall()
        return None
