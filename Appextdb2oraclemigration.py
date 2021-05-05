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
        s= self.get_plugin()
        #logging.info(str(s.get_plugin_directory()))
        try:
            self.xmlfile =str(s.get_plugin_directory())+ "\\parsedefine.xml" 
            if (os.path.isfile(self.xmlfile)):
                        tree = ET.parse(self.xmlfile, ET.XMLParser(encoding="UTF-8"))
                        root=tree.getroot()
            logging.debug(str(self.xmlfile));
        except ET.ParseError as err:
            logging.info(": error  saving property violation   : %s", str(err))  
            return tree
        for o in application.search_objects(category='sourceFile'):
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            if not (o.get_path().endswith('.sql')):
                continue
            #cast.analysers.log.debug("file found: >" + str(o.get_path()))
            logging.debug("file found: >" + str(o.get_path()))
            if (o.get_path().endswith('.sql')):
                self.getsqlsearch(o, application, root)
            
            
                
        for o in application.search_objects(category='JV_FILE'):
      
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if not (o.get_path().endswith('.java')):
                continue
            #cast.analysers.log.debug("file found: >" + str(o.get_path()))
            logging.debug("file found: >" + str(o.get_path()))
             
            if (o.get_path().endswith('.java')):  
                self.getJavafilesearch(o, application, root)
                 
                 
        for o in application.search_objects(category='sourceFile'):
           
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if not (o.get_path().endswith('.properties')):
                continue
            #cast.analysers.log.debug("file found: >" + str(o.get_path()))
            logging.debug("file found: >" + str(o.get_path()))
         
            if (o.get_path().endswith('.properties')):
                self.getpropertiessearch(o, application, root)
                
       
#             
            #self.scan_Sql(application, o)               
            
    def getsqlsearch(self,  file, application, root): 
        logging.info("file sql start")
       
        try:
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
                                self.setpropjavasql(application, file, sobjname, sviolation); 
                                
        except Exception as e:
            logging.info(": error  db2Sql extension  set : %s", str(e))  
            return  
        
        
    def getpropertiessearch(self,  file, application, root): 
        logging.info("Properties java start")
       
        try:
                    for group in root.findall('propertiesfileSearch'):
                        self.sregex = unescape(group.find('RegexPattern').text)
                        logging.debug("---"+str(self.sregex)+ "---")
                                   
                        if file.get_name().endswith('.properties'):
                            logging.info('Scanning properties  file :'+str(Path(file.get_path()).name))
                            if (os.path.isfile(file.get_path())):
                                sobjname = group.find('propertyname').text 
                                self.currentsrcfile= file
                                self.sgobjname=sobjname
                                sviolation = group.find('Rulename').text 
                                logging.debug(str(sobjname)+"Reg ex--->"+str(self.sregex) )
                                self.setprop(application, file, sobjname, sviolation); 
                                
        except Exception as e:
            logging.info(": error  db2Sql extension  properties search  : %s", str(e))  
            return  
                                
    def getJavafilesearch(self,  file, application, root): 
        logging.info("java file start")
       
        try:
                    for group in root.findall('javafileSearch'):
                        self.sregex = unescape(group.find('RegexPattern').text)
                        logging.debug("---"+str(self.sregex)+ "---")
                                   
                        if file.get_name().endswith('.java'):
                            logging.info('Scanning java  file :'+str(Path(file.get_path()).name))
                            if (os.path.isfile(file.get_path())):
                                sobjname = group.find('propertyname').text 
                                self.currentsrcfile= file
                                self.sgobjname=sobjname
                                sviolation = group.find('Rulename').text 
                                logging.debug(str(sobjname)+"Reg ex--->"+str(self.sregex) )
                                self.setpropjavasql(application, file, sobjname, sviolation); 
                                      
        except Exception as e:
            logging.info(": error  db2Sql extension  java search  : %s", str(e))  
            return  
        # Final reporting in ApplicationPlugins.castlog
        
    def setpropjavasql(self, application, file, sobjname, rulename):
            # one RF for multiples patterns
            
            rfCall = ReferenceFinder()
            rfCall.add_pattern(('srcline'),before ='' , element =self.sregex, after = '')     # requires application_1_4_7 or above
            
            # search all patterns in current program
            try:
                #self.propvalue =[]
                #getvalue=""
                cntj= 0
                references = [reference for reference in rfCall.find_references_in_file(file)]
                for  reference in references:
                    reference.bookmark.file= file
                    linenb=int(str(reference.bookmark).split(',')[2])
                    #logging.debug( str(reference.bookmark).split(',')[2])
                    #logging.debug("Specific object:"+ str(file.find_most_specific_object(linenb, 1)))
                    obj = file.find_most_specific_object(linenb, 1)
                    cntj =cntj+1
                    #self.propvalue.append(str(reference.value)+" "+str(reference.bookmark))
                    obj.save_violation('dboraclemigration_CustomMetrics.'+ rulename, reference.bookmark)
                    logging.debug("violation saved: >" +'dboraclemigration_CustomMetrics.'+rulename+"  line:::"+str(reference.value)+str(reference.bookmark))
                            #break
#                     file.save_property('dboraclemigrationScript.'+sobjname, reference.value+" "+str(reference.bookmark) )
#                     logging.info("property saved: >" +'dboraclemigrationScript.'+sobjname +" "+str(reference.bookmark)+ ' '+ str(reference.value))
                #getvalue="".join(self.propvalue)
                #logging.debug("Value of list-->"+ str(getvalue))
                if cntj>0:
                    obj.save_property('dboraclemigrationScript.'+sobjname, str(cntj))
                    logging.debug("property saved: --->" +'dboraclemigrationScript.'+sobjname +" "+str(cntj))
               
#       
            except Exception as e:
                logging.info(": error  saving property violation   : %s", str(e))  
                return 
            
    def setprop(self, application, file, sobjname, rulename):
            # one RF for multiples patterns
            
            rfCall = ReferenceFinder()
            rfCall.add_pattern(('srcline'),before ='' , element =self.sregex, after = '')     # requires application_1_4_7 or above
            
            # search all patterns in current program
            try:
#                 self.propvalue =[]
#                 getvalue=""
                cntprop= 0
                references = [reference for reference in rfCall.find_references_in_file(file)]
                for  reference in references:
                    reference.bookmark.file= file
                    cntprop =cntprop+1
                    #self.propvalue.append(str(reference.value)+" "+str(reference.bookmark))
                    file.save_violation('dboraclemigration_CustomMetrics.'+ rulename, reference.bookmark)
                    logging.debug("violation saved: >" +'dboraclemigration_CustomMetrics.'+rulename+"  line:::"+str(reference.value)+str(reference.bookmark))
                            #break
#                     file.save_property('dboraclemigrationScript.'+sobjname, reference.value+" "+str(reference.bookmark) )
#                     logging.info("property saved: >" +'dboraclemigrationScript.'+sobjname +" "+str(reference.bookmark)+ ' '+ str(reference.value))
#                 getvalue="".join(self.propvalue)
                #logging.debug("Value of list-->"+ str(getvalue))
                if cntprop >0:
                    file.save_property('dboraclemigrationScript.'+sobjname, str(cntprop))
                    logging.debug("property saved: --->" +'dboraclemigrationScript.'+sobjname +" "+str(cntprop))
               
#       
            except Exception as e:
                logging.info(": error  saving property violation on properties  : %s", str(e))  
                return 
            
     
    
    def setdeclareproperty(self, application):
        
        declarelist=['sourceFile', 'SQLScriptSchema','SQLScriptTable','SQLScriptTableColumn','SQLScriptIndex',
                     'SQLScriptProcedure','SQLScriptDML','SQLScriptFunction','SQLScriptView','SQLScriptTrigger',
                     'SQLScriptPackage','SQLScriptType','SQLScriptForeignKey','SQLScriptUniqueConstraint','SQLScriptEvent',
                     'SQLScriptSynonym','SQLScriptTableSynonym','SQLScriptViewSynonym','SQLScriptFunctionSynonym',
                     'SQLScriptProcedureSynonym','SQLScriptPackageSynonym','SQLScriptTypeSynonym','SQLScriptMethod','JV_METHOD', 'JV_GENERIC_METHOD', 
                     'JV_INST_METHOD', 'JV_INST_CLASS', 'JV_CTOR', 'JV_GENERIC_CTOR', 'JV_FILE', 'JV_INST_CTOR', 'JV_INTERFACE', 'JV_GENERIC_INTERFACE', 
                     'JV_INST_INTERFACE', 'JV_GENERIC_CLASS','JV_PROJECT', 'JV_PACKAGE', 'JV_CLASS']
        for declareitems in declarelist: 
                application.declare_property_ownership('dboraclemigrationScript.CONCAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NEXT_VALUE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RESULT_SET_LOCATOR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DAYS',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MINUTES',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SYSDUMMY1',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.WITH_UR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.FETCH',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.EXCEPT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.ATANH',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BIGINT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BITANDNOT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BITOR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BITNOT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BITXOR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.BLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CHARACTER_LENGTH',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CHAR_LENGTH',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.COT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CURRENT_DATE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CURRENT_SERVER',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SQLID',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TIME',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CURRENT_USER',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CURSOR_ROWCOUNT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DAY',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DAYNAME',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DAYOF',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DBCLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DECFLOAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DECIMAL',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DIGITS',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DOUBLE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.EMPTY_DBCLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.EMPTYNCLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.FLOAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.HEX',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.HOUR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.INSERT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.INT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.JULIAN',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LCASE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LEFT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LOCATE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LOG10',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LONG_VARCHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LONG_VARGRAPHIC',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MAX',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MIN',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MINUTE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MONTH',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MONTHNAME',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MULTIPLY_ALT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MICROSECOND',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.MIDNIGHT_SECONDS',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NCHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NCLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NVARCHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NVL',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.OCT_LENGHT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.QUARTER',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RADIANS',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RAISE_ERROR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RAND',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.FunctionREAL',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.REPEAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RIGHT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SECOND',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.FunctionSMALLINT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SPACE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.STRIP',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TIMEStamp',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TIMESTAMPDIFF',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TRUNC_TIMESTAMP',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TRUNCATE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.UCASE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VALUE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARCHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARCHAR_BIT_FORMER',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FORMAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FORMAT_BIT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARGRAPHIC',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.WEEK',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLDOCUMENT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLNAMESPACES',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLROW',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLTEXT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLVALIDATE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XMLXMLXSROBJECTID',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.YEAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEBIGINT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CHAR_FOR_BIT_DATA',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.CHAACTER_VARYING',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEDBCLOB',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEDECIMAL',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEDECFLOAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEFLOAT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEGRAPHIC',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.INTEGER',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NCHAR_VARYING',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.NUMERIC',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.REAL',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SMALLINT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPETIME',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.DATATYPEVARCHAR',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARCHAR_FOR_BIT_DATA',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.VARGRAPHIC',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.XML',[declareitems])
                # Added By Julien
                application.declare_property_ownership('dboraclemigrationScript.SNAPSHOT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LOAD',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.dynexpln',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.SNAP',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.IMPORT_EXPORT',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.db2HistoryFcts',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.REGEXP_REPLACE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.HEXTORAW',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LOCALTIMESTAMP',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.GLOBAL_TEMPORARY_TABLE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LISTAGG',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LPAD',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.LTRIM',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.OVERLAY',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.REPLACE',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RPAD',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.RTRIM',[declareitems])
                application.declare_property_ownership('dboraclemigrationScript.TRANSLATE',[declareitems])
                #end
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Built_in_SQL_Functions_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.SQL_language_elements_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Datetime_interval_expressions_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Data_Types_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.SELECT_Statement_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.CREATE_TABLE_statement_variations',[declareitems])