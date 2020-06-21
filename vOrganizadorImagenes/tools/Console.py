#!/bin/python
import argparse
import logging
from .Organizador import Organizador

class Console(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None
    
    def argumentParse(self):
        self.parser.add_argument("--cli", help="Modo consola",action="store_true",default=False)
        self.parser.add_argument("--ws", help="Modo Web Service",action="store_true",default=False)
        self.parser.add_argument("--dirs-input",help="Directorios de entrada", nargs="+", type=str)
        self.parser.add_argument("--dir-out",help="Directorio de salida", nargs="?", type=str)
        self.parser.add_argument('--debug',default=True, action="store_true", help='modo debug')
        self.args = self.parser.parse_args()
    
    def iniciar(self):
        self.argumentParse()
        print(self.args)
        organizador = Organizador(dirsInput=self.args.dirs_input,dirOutput=self.args.dir_out)
        organizador.procesarDirsInput()