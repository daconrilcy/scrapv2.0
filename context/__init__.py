import re
import glob,os
import tools

class DatabaseInfo:
    host = None
    user = None
    password = None
    database = None


class Env:
    database = DatabaseInfo()
    brands = []

    def __init__(self):
        self._loadFileEnv()

    def _loadFileEnv(self):
        datas = {}
        objs = []
        with open('context/env.txt', 'r') as fileopen:
            lines = fileopen.readlines()
            objEnCours = ""
            for line in lines:
                clearline = re.sub("[\s\n\:]*", "", line)
                if line[0:1] == "#":
                    objEnCours = clearline[1:]
                    datas[objEnCours] = {}
                    objs.append(objEnCours)
                else:
                    if objEnCours != "":
                        splitted = clearline.split("=")
                        if len(splitted) == 2:
                            datas[objEnCours][splitted[0]] = splitted[1]
                        else:
                            if splitted[0] != '':
                                if not isinstance(datas[objEnCours], list):
                                    datas[objEnCours] = []
                                datas[objEnCours].append(splitted[0])
        self._convertEnvDictToEnvObj(datas)

    def _convertEnvDictToEnvObj(self, envDict: dict):
        if 'database' in envDict.keys():
            self.database.host = envDict['database']['host']
            self.database.user = envDict['database']['user']
            self.database.password = envDict['database']['password']
            self.database.database = envDict['database']['database']
        if 'brands' in envDict.keys():
            for b in envDict['brands']:
                self.brands.append(b)

    def printObj(self):
        print( self.database.host)
        print(self.database.user)
        print(self.database.password)
        print( self.database.database)
        print('brands: ')
        for b in self.brands:
            print(b)