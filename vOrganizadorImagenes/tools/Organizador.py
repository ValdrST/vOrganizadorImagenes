import os
import logging
import pathlib
import hashlib
import shutil
import threading
from .DataBase import DataBase
from exif import Image
#logging.basicConfig(level=logging.ERROR)
class Organizador():
    def __init__(self, dirsInput=[], dirOutput=None):
        self.dirsInput = dirsInput
        self.dirOutput = dirOutput
        self.tipos = [".jpg",".jpeg",".png",".bmp",".raw",".tga","gif"]
        self.dataBaseFile = "base.db"
        self.db = DataBase(self.dataBaseFile)
        self.db.crearBase()
    
    def procesarDirsInput(self):
        for directorio in self.dirsInput:
            self.getPathFotos(directorio = directorio)

    def getPathFotos(self,directorio):
        for root, dirs, files in os.walk(directorio):
            for filename in files:
                t = threading.Thread(target=self.getDatosFoto,args=(os.path.join(root, filename),))
                t.start()
                t.join()

    def getDatosFoto(self, filename):
        foto = {"fileName":filename,
                "hash":None, 
                "hasExif":0, 
                "hasDateTime":0, 
                "corruptExif":0,
                "newFileName":""
                }
        ext = pathlib.PurePosixPath(filename).suffix.lower()
        if ext in self.tipos:
            try:
                with open(filename, 'rb') as image_file:
                    my_image = Image(image_file)
                    foto["hash"] = self.getCheckSum(image_file)
                    if my_image.has_exif:
                        foto["hasExif"] = 1
                        if "datetime" in dir(my_image):
                            nombreNuevo = self.generarNombreFoto(my_image.datetime)
                        elif "datetime_original" in dir(my_image):
                            nombreNuevo = self.generarNombreFoto(my_image.datetime_original)
                        else:
                            logging.warning("Imagen {} sin dato de fecha. Alternativas {}".format(filename, dir(my_image)))
                            raise Exception
                        foto["newFileName"] = nombreNuevo
                        foto["hasDateTime"] = 1
                        try:
                            if not os.path.isfile(self.dirOutput + "\\"+ nombreNuevo + ext):
                                shutil.copy(filename, self.dirOutput + "\\"+ nombreNuevo + ext)
                            else:
                                logging.warning("Imagen repetida {}".format(filename))
                            logging.info("Imagen {} procesada de forma exitosa.".format(filename))
                        except Exception as e:
                            logging.error("Error al copiar {} {} {}".format(filename,self.dirOutput + "\\"+ nombreNuevo + ext,e))   
                    else:
                        logging.info("Imagen {} sin datos exif".format(filename))
            except Exception as e:
                foto["corruptExif"] = 1
                logging.error("Error con esta imagen {} {}".format(filename, e))
            finally:
                pass
                #if len(self.db.getConHash(foto["hash"])) == 0:
                #    self.db.insertarFoto(foto)
                #else:
                #    self.db.actualizarFoto(foto)
                #self.db.conn.commit()
        else:
            logging.info("Archivo no es imagen {}".format(filename))
        

    
    def generarNombreFoto(self, fechaHora):
        nombre = "IMG_"+fechaHora
        nombre = nombre.replace(":","")
        nombre = nombre.replace("/","")
        nombre = nombre.replace(" ","_")
        nombre = nombre.replace('\0',"")
        return nombre

    def getCheckSum(self,f):
        data = f.read()
        return hashlib.blake2b(data).hexdigest()

if __name__ == "__main__":
    organizador = Organizador(dirsInput=["D:\\Disco_nark\\Imagenes"])
    organizador.procesarDirsInput()
