import os
import logging
import pathlib
import hashlib
from .DataBase import DataBase
from exif import Image

class Organizador():
    def __init__(self, dirsInput=[], dirOutput=None):
        self.dirsInput = dirsInput
        self.dirOutput = dirOutput
        self.tipos = [".jpg",".jpeg",".png",".bmp",".raw",".tga"]
        self.dataBaseFile = "base.db"
        self.db = DataBase(self.dataBaseFile)
        self.db.crearBase()
    
    def procesarDirsInput(self):
        for directorio in self.dirsInput:
            self.getPathFotos(directorio = directorio)

    def getPathFotos(self,directorio):
        for root, dirs, files in os.walk(directorio):
            for filename in files:
                self.getDatosFoto(directorio+"\\"+filename)
            for dirRec in dirs:
                self.getPathFotos(dirRec)

    def getDatosFoto(self, filename):
        foto = {"fileName":filename,
                "hash":None, 
                "hasExif":0, 
                "hasDateTime":0, 
                "corruptExif":0
                }
        ext = pathlib.PurePosixPath(filename).suffix
        if ext in self.tipos:
            try:
                with open(filename, 'rb') as image_file:
                    foto["hash"] = self.getCheckSum(image_file)
                    my_image = Image(image_file)
                    if my_image.has_exif:
                        try:
                            foto["hasExif"] = 1
                            self.generarNombreFoto(my_image.datetime)
                            foto["hasDateTime"] = 1
                        except:
                            print(dir(my_image))
                            logging.warning("imagen {} sin dato de fecha".format(filename))
                    else:
                        logging.warning("imagen {} sin datos exif".format(filename))
            except Exception as e:
                foto["corruptExif"] = 1
                logging.error("Error con esta imagen {} {}".format(filename, e))
            finally:
                if len(self.db.getConHash(foto["hash"])) == 0:
                    self.db.insertarFoto(foto)
                else:
                    print(foto)
                    print(self.db.getConHash(foto["hash"]))
        self.db.conn.commit()

    
    def generarNombreFoto(self, fechaHora):
        nombre = "IMG_"+fechaHora
        nombre = nombre.replace(":","")
        nombre = nombre.replace(" ","_")
        print(nombre)

    def getCheckSum(self,f):
        data = f.read()
        return hashlib.blake2b(data).hexdigest()

if __name__ == "__main__":
    organizador = Organizador(dirsInput=["D:\\Disco_nark\\Imagenes"])
    organizador.procesarDirsInput()
