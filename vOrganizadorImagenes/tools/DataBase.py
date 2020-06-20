#!/bin/python
import sqlite3
import logging
class DataBase():
    def __init__(self, dbFile):
        self.conn = sqlite3.connect(dbFile)
    
    def crearBase(self):
        try:
            self.ejecutarSentencia("CREATE TABLE fotos (fileName TEXT, hash TEXT PRIMARY KEY, hasExif Integer, hasDateTime Integer, corruptExif Integer, newFileName TEXT)")
            self.conn.commit()
        except:
            logging.info("Base de datos ya existente")

    def ejecutarSentencia(self, query=None):
        if query != None:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()

    def insertarFoto(self,foto):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO fotos (fileName, hash, hasExif, hasDateTime, corruptExif) VALUES (?,?,?,?,?)',
        (foto["fileName"], foto["hash"], foto["hasExif"], foto["hasDateTime"], foto["corruptExif"]))

    def getConHash(self,hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fotos WHERE hash=?",(hash,))
        return cursor.fetchall()

    def cerrarBase(self):
        self.conn.close()

if __name__ == "__main__":
    db = DataBase(dbFile="base.db")
    db.ejecutarSentencia("CREATE TABLE fotos (fechahora TEXT, hash TEXT)")
    db.cerrarBase()
