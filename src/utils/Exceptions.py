# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        	Gazetter V3.0
# Purpose:		Aproximador de sitios de interes Colombia
#
# Author:      	Harold Avenia - Esri Colombia.
#
# Created:     	14/06/2017
# Last Edition: 13/10/2017
# Copyright:   	(c) Esri Colombia 2017
# Licence:    	Arcpy
# -------------------------------------------------------------------------------
"""---------------------------Import Libraries --------------------------------"""
import sys, traceback

"""-------------------------Configuración------------------------------------"""

"manejador de excepciones"


class Exceptions(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


"captura los eventos cuando se lanza excepciones"


def getTraceBack():
    err = ""
    tb = sys.exc_info()[2]
    if tb:
        tbinfo = traceback.format_tb(tb)[0]
        try:
            err = u'%s%s' % (tbinfo, sys.exc_info())
        except:
            try:
                err = tbinfo
            except:
                err = "Error inesperado."
    return err
