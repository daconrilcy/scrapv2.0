from files.paths import OtherFilePath
from files.paths import BrandFilesPath

Nvidia = BrandFilesPath(brand='Nvidia')
Asus = BrandFilesPath(brand='Asus')
Gigabyte = BrandFilesPath(brand='Gigabyte')
Amd = BrandFilesPath(brand='Amd')
Evga = BrandFilesPath(brand='EVGA')
Babadazd = BrandFilesPath(brand='babadazd')


class FileNamesModel:
    other = OtherFilePath()
    Nvidia = Nvidia
    Asus = Asus
    Gigabyte = Gigabyte
    Amd = Amd
    Evga = Evga
    Babadazd = Babadazd


FilesNames = FileNamesModel()
