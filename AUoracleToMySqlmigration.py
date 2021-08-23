import cast.analysers.ua
from cast.analysers import log as Print
from cast.application import   ReferenceFinder
import re
import os
import random
from pathlib import Path


class oracleToMySqlmigrationExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.package = ""
        self.classname = ""
        self.file = ""    
        self.initial_crc =  None
        self.file_ref=""
        self.extnls=[]
        self.parentOBJ=None
        self.parentOBJtwo=None
        self.counter = ""
        return

    def start_analysis(self):
        Print.info("oracleToMySqlmigration : Running extension code start")
       
    
    
        
    def end_analysis(self):
        Print.info("oracleToMySqlmigration : Running extension code end")
       
        pass