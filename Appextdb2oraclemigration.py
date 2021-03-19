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
                file.save_property('dboraclemigrationScript.'+sobjname, str(getvalue))
                logging.info("property saved: --->" +'dboraclemigrationScript.'+sobjname +" "+str(getvalue))
               
#       
            except ValueError:
                    logging.info ("error saving property")
    
    def setdeclareproperty(self, application):
        application.declare_property_ownership('dboraclemigrationScript.CONCAT',["sourceFile"])
        #application.declare_property_ownership('dboraclemigrationScript.NEXT_VALUE',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.RESULT_SET_LOCATOR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.FETCH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.EXCEPT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.ATANH',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BIGINT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITANDNOT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.TIME',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.BITOR',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DECFLOAT',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.CLOB',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DECIMAL',["sourceFile"])
        application.declare_property_ownership('dboraclemigrationScript.DATE',["sourceFile"])
        
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Built_in_SQL_Functions_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.SQL_language_elements_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Datetime_interval_expressions_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.Data_Types_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.SELECT_Statement_variations',["sourceFile"])
        application.declare_property_ownership('dboraclemigration_CustomMetrics.CREATE_TABLE_statement_variations',["sourceFile"])
       