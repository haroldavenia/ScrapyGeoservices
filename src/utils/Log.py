# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        	Gazetter V3.0
# Purpose:		Write errors o sucessful in text file
#
# Author:      	Harold Avenia - Esri Colombia.
#
# Created:     	14/06/2017
# Last Edition: 13/10/2017
# Copyright:   	(c) Esri Colombia 2017
# Licence:    	Arcpy
# -------------------------------------------------------------------------------
"""---------------------------Import Libraries --------------------------------"""
import os
from datetime import datetime
from src.utils.Exceptions import *

"""-------------------------Configuración------------------------------------"""
path = os.getcwd()
sys.path.append(path)
scriptPath = sys.path[0]
"""-------------------------------Class--------------------------------------"""
"Clase que crea un archivo log"


class Log(object):
    "Atributos de la clase"
    logFilePath = ""
    _numberErros = 0
    _instances = {}

    "Constructor"

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Log, class_).__new__(class_, *args, **kwargs)
            class_._instances[class_].createLogFile()
        return class_._instances[class_]

    def getErrorsCount(self):
        return self._numberErrors

    "Registra los eventos en el archivo log del sistema"

    def writeLog(self, message):
        # Se abre el archivo
        if os.path.exists(self.logFilePath):
            log = open(self.logFilePath, "a")
            # Se escribe en el archivo
            try:
                log.write(message)
                log.write("\n")
                return True
            except Exception as exception:
                # no se puedo controlar el error
                message = u"No se puede continuar con la búsqueda debido a que se encontrarón caracteres invalidados"
                exception = Exceptions(getTraceBack())
                raise exception
            finally:
                log.close()
        else:
            message = u"No se pudo escribir en el archivo log"
            exception = Exceptions(getTraceBack())
            raise exception

    "Registra los eventos de error en el archivo log del sistema"

    def writeLogError(self, Error):
        # escribe en el log los errores
        try:
            if self.writeLog(Error):
                self._numberErros += 1
        except:
            message = u"No se pudo escribir el error en el archivo log"
            exception = Exceptions(getTraceBack())
            raise exception

    "Remueve el archivo Log"

    def removeLog(self):
        try:
            # Si existe el archivo lo remueve
            if os.path.isfile(self.logFilePath):
                os.remove(self.logFilePath)
        except:
            # raise self._excepts.Error(self._excepts.getTraceBack())
            message = u"No se pudo elminiar el archivo log"
            exception = Exceptions(getTraceBack())
            raise exception

    "Crea el archivo de texto"

    def createLogFile(self, current_path=os.path.dirname(os.path.abspath(__file__))):
        try:
            # Si existe el archivo lo remueve
            if os.path.isfile(self.logFilePath):
                os.remove(self.logFilePath)
                return True
            else:
                today = datetime.today()
                message = "Creacion archivo log... \n " + str(today)
                pDate = today.strftime("%Y-%m-%d_%H-%M-%S")
                self.logFilePath = os.path.join(current_path, "LOG_%s.log" % pDate)
                log = open(self.logFilePath, "w")
                log.write("LOG GEOTWITTER\n")
                log.close()
        except:
            message = u"No se pudo crear el archivo log"
            exception = Exceptions(getTraceBack())
            raise exception
