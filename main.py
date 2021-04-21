from interface import *
from events import Events
from controller import Controller
from routeur import Router
import threading
from files import ActionFile
from controller.importGigabyte import ImportGigabyte
import requests
import json
from tools import *
from database import ORM
from database.entity import *
from database import Entity
from context import *
from database.annotation import EntityAnnotation
from database.entityManager import EntityManager

from database import FieldTable, FieldTableTypes
from database.annotation import convertAttibuteToField
from database.ORM import ORM

import re, os, glob, random


"""
gig = ImportGigabyte()
gig.importDatas()
gig.traitements()

a = ActionFile()
b = ['official']
m = a.loadDataBruteJsonToFile(fileName=a.fileNames.other.fieldsAbsent)

print(m)

r = BrandEntity()
r.setNom("babadazd")
r.setSiteweb("www.kapodzakdp.com")

v = BrandEntity()
v.setNom("zezezeze")
v.setSiteweb("www.peop.fr")

w = CarteGraphiqueEntity()
w.setPsu(500)
w.setSlot(2.5)
w.setWidth(400)
w.setHeight(200)
w.setBoostclock(2000)

em = EntityManager()
em.persist(r)
#em.persist(v)
em.persist(w)
print(em._request)
aa = em.getById(5)
bb = em.getallBy(requestChain=[('nom', ["Nvidia", "Gigabyte"])], entity=BrandEntity())
for b in bb:
    print(str(b.getId()) + ":"+ b.getNom())

b = EntityManager()
b.migrations.migrateAllFromMysql()
c = b.getById(entity=BrandEntity(), idInTable=3)
ds = b.getallBy(requestChain=[("nom", ["Gigabyte", "Asus"])], entity=BrandEntity())
es = b.getAll()
"""

from files.paths import updateFilesBrand
from files.paths.pathclass import *
from files.fields import loadBrandFields

g = ImportGigabyte()
g.importDatas()
for f in g.fields_pre_List:
    print(f)