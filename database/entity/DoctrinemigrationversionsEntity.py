import datetime
from database import Entity


# @ORM/EntityName=doctrine_migration_versions
class DoctrinemigrationversionsEntity(Entity):
    # ###
    # @ORM/FieldName=version
    # @ORM/Column(type=varchar,length=191,key=PRI,nullable=NO)
    # ###
    _version: str = None

    # ###
    # @ORM/FieldName=executed_at
    # @ORM/Column(type=date,nullable=YES)
    # ###
    _executedAt: datetime.date = None

    # ###
    # @ORM/FieldName=execution_time
    # @ORM/Column(type=int,nullable=YES)
    # ###
    _executionTime: int = None

    def getVersion(self):
        return self._version

    def getExecutedat(self):
        return self._executedAt

    def setExecutedat(self, executedAt: datetime.date):
        self._executedAt = executedAt
        return self

    def getExecutiontime(self):
        return self._executionTime

    def setExecutiontime(self, executionTime: int):
        self._executionTime = executionTime
        return self
