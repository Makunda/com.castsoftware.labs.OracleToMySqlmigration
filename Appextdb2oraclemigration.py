import cast_upgrade_1_6_5 # @UnusedImport
from cast.application import ApplicationLevelExtension, ReferenceFinder
import logging
import xml.etree.ElementTree as ET
import re
import os
import random
from html import unescape
from pathlib import Path


class db2oraclemigrationExtensionApplication(ApplicationLevelExtension):

    def __init__(self): 
        self.currentsrcfile=""
        self.sregex = ""
        self.sgobjname=""
        self.filename = ""
        self.xmlfile = ""
        self.file = ""    
        self.propvalue=[]
        pass     
    
    
            
        
        
    def end_application(self, application):
        logging.debug("running code at the end of an application in db2oraclemigration")
        self.setdeclareproperty(application);
        for o in application.search_objects(category='sourceFile'):
          
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
           
            if not (o.get_path().endswith('.sql')):
                continue
            #cast.analysers.log.debug("file found: >" + str(o.get_path()))
            logging.debug("file found: >" + str(o.get_path()))
            self.getconfigsearch(o, application)
            #self.scan_Sql(application, o)               
            
    def getconfigsearch(self,  file, application): 
        logging.info("file start")
        s= self.get_plugin()
        #logging.info(str(s.get_plugin_directory()))
        self.xmlfile =str(s.get_plugin_directory())+ "\\parsedefine.xml" 
        logging.debug(str(self.xmlfile));
        try:
           
            if (os.path.isfile(self.xmlfile)):
                    tree = ET.parse(self.xmlfile, ET.XMLParser(encoding="UTF-8"))
                    root=tree.getroot()
                    
                    for group in root.findall('Search'):
                        self.sregex = unescape(group.find('RegexPattern').text)
                        logging.debug("---"+str(self.sregex)+ "---")
                                   
                        if file.get_name().endswith('.sql'):
                            logging.info('Scanning sql  file :'+str(Path(file.get_path()).name))
                            if (os.path.isfile(file.get_path())):
                                sobjname = group.find('propertyname').text 
                                self.currentsrcfile= file
                                self.sgobjname=sobjname
                                sviolation = group.find('Rulename').text 
                                logging.debug(str(sobjname)+"Reg ex--->"+str(self.sregex) )
                                self.setprop(application, file, sobjname, sviolation); 
                                
        except Exception as e:
            logging.debug(": error  db2Sql extension  set : %s", str(e))  
            return  
        # Final reporting in ApplicationPlugins.castlog
        
    def setprop(self, application, file, sobjname, rulename):
            # one RF for multiples patterns
            
            rfCall = ReferenceFinder()
            rfCall.add_pattern(('srcline'),before ='' , element =self.sregex, after = '')     # requires application_1_4_7 or above
            
            # search all patterns in current program
            try:
                self.propvalue =[]
                getvalue=""
                references = [reference for reference in rfCall.find_references_in_file(file)]
                for  reference in references:
                    reference.bookmark.file= file
                    self.propvalue.append(str(reference.value)+" "+str(reference.bookmark))
                    file.save_violation('dboraclemigration_CustomMetrics.'+ rulename, reference.bookmark)
                    logging.debug("violation saved: >" +'dboraclemigration_CustomMetrics.'+rulename+"  line:::"+str(reference.value)+str(reference.bookmark))
                            #break
#                     file.save_property('dboraclemigrationScript.'+sobjname, reference.value+" "+str(reference.bookmark) )
#                     logging.info("property saved: >" +'dboraclemigrationScript.'+sobjname +" "+str(reference.bookmark)+ ' '+ str(reference.value))
                getvalue="".join(self.propvalue)
                #logging.debug("Value of list-->"+ str(getvalue))
                if len(getvalue) >0:
                    file.save_property('dboraclemigrationScript.'+sobjname, str(getvalue))
                    logging.info("property saved: --->" +'dboraclemigrationScript.'+sobjname +" "+str(getvalue))
               
#       
            except ValueError:
                    logging.info ("error saving property")
    
    def setdeclareproperty(self, application):
        application.declare_property_ownership('dboraclemigrationScript.CONCAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NEXT_VALUE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RESULT_SET_LOCATOR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DAYS',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MINUTES',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.SYSDUMMY1',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.WITH_UR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.FETCH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.EXCEPT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.ATANH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BIGINT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITANDNOT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITOR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITNOT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITXOR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CHARACTER_LENGTH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CHAR_LENGTH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.COT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CURRENT_DATE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CURRENT_SERVER',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.SQLID',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TIME',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CURRENT_USER',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CURSOR_ROWCOUNT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DAY',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DAYNAME',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DAYOF',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DBCLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DECFLOAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DECIMAL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DIGITS',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DOUBLE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.EMPTY_DBCLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.EMPTYNCLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.FLOAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.HEX',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.HOUR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.INSERT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.INT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.JULIAN',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LCASE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LEFT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LOCATE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LOG10',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LONG_VARCHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.LONG_VARGRAPHIC',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MAX',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MIN',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MINUTE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MONTH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MONTHNAME',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MULTIPLY_ALT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MICROSECOND',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.MIDNIGHT_SECONDS',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NCHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NCLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NVARCHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NVL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.OCT_LENGHT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.QUARTER',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RADIANS',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RAISE_ERROR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RAND',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.FunctionREAL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.REPEAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RIGHT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.SECOND',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.FunctionSMALLINT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.SPACE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.STRIP',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TIMEStamp',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TIMESTAMPDIFF',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TRUNC_TIMESTAMP',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TRUNCATE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.UCASE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VALUE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARCHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARCHAR_BIT_FORMER',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FORMAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FORMAT_BIT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARGRAPHIC',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.WEEK',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLDOCUMENT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLNAMESPACES',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLROW',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLTEXT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLVALIDATE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XMLXMLXSROBJECTID',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.YEAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEBIGINT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CHAR_FOR_BIT_DATA',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CHAACTER_VARYING',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEDBCLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEDECIMAL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEDECFLOAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEFLOAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEGRAPHIC',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.INTEGER',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NCHAR_VARYING',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.NUMERIC',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.REAL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.SMALLINT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPETIME',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATATYPEVARCHAR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FOR_BIT_DATA',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.VARGRAPHIC',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.XML',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Built_in_SQL_Functions_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.SQL_language_elements_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Datetime_interval_expressions_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Data_Types_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.SELECT_Statement_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.CREATE_TABLE_statement_variations',["sourceFile"])  