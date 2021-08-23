import cast_upgrade_1_6_5 # @UnusedImport
from cast.application import ApplicationLevelExtension, ReferenceFinder
import logging
import xml.etree.ElementTree as ET
import re
import os
import random
from html import unescape
from pathlib import Path


class oracleToMySqlmigrationExtensionApplication(ApplicationLevelExtension):

    def __init__(self): 
        self.currentsrcfile=""
        self.sregex = ""
        self.sgobjname=""
        self.filename = ""
        self.xmlfile = ""
        self.file = ""    
        self.propvalue=[]
        self.uniqueobjlist =[]
        pass     
    
        
    def end_application(self, application):
        logging.debug("running code at the end of an application in oracleToMySqlmigration")
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
                        logging.debug("---" + str(self.sregex) + "---")
                                   
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
        logging.info("Java Scan start")
       
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
                self.propvalue =[]
                self.uniqueobjlist =[]
                cntj= 0
                references = [reference for reference in rfCall.find_references_in_file(file)]
                for  reference in references:
                    reference.bookmark.file= file
                    linenb=int(str(reference.bookmark).split(',')[2])
                    #logging.debug( str(reference.bookmark).split(',')[2])
                    #logging.debug("Specific object:"+ str(file.find_most_specific_object(linenb, 1)))
                    obj = file.find_most_specific_object(linenb, 1)
                    cntj =cntj+1
                    self.uniqueobjlist.append(sobjname + "cast" +str(obj))
                    obj.save_violation('dboraclemigration_CustomMetrics.'+ rulename, reference.bookmark)
                    #logging.debug("violation saved: >" +'dboraclemigration_CustomMetrics.'+rulename+"  line:::"+str(reference.value)+str(reference.bookmark))
                            #break
#                     file.save_property('dboraclemigrationScript.'+sobjname, reference.value+" "+str(reference.bookmark) )
#                     logging.info("property saved: >" +'dboraclemigrationScript.'+sobjname +" "+str(reference.bookmark)+ ' '+ str(reference.value))
                                #logging.info('unique' + str(self.uniqueobjlist))
                self.unique(self.uniqueobjlist,application)
              #       
            except Exception as e:
                logging.info(": error  saving property violation   : %s", str(e))  
                return 
            
            # function to get unique values
    def unique(self, objcastlist, application):
       
        unique_list = []
        #logging.info(str(objcastlist))
       
       
        for x in objcastlist:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                  
        for x in unique_list:
            logging.debug('{} has occurred {} times'.format(x, self.countcastobject(objcastlist, x)))
            logging.debug(x)
            orgx=x
            x= x.replace('castObject', ',')
            x=x.replace('(', '')
            x= x.replace(')', '')
            dbtype = x.split(',')[0].strip()
            objname= x.split(',')[1].strip()
            objcatergory =x.split(',')[2].strip()
            if objname.find('.') is not -1:
                objname = objname.split('.')[1]
            MethodObjectReferences = list(application.search_objects(category=objcatergory,  name=objname,  load_properties=True))
            if len(MethodObjectReferences)>0:
                for obj in MethodObjectReferences : 
                    cnt = str(self.countcastobject(objcastlist, orgx))
                    obj.save_property('dboraclemigrationScript.'+dbtype, cnt)
                    logging.debug("property saved: --->" +'dboraclemigrationScript.'+dbtype +" "+cnt)  
                        
    def countcastobject(self, lst, x):
        count = 0
        for ele in lst:
            if (ele == x):
                count = count + 1
        return count
         
        
        
            
    def setprop(self, application, file, sobjname, rulename):
            # one RF for multiples patterns
            
            rfCall = ReferenceFinder()
            rfCall.add_pattern(('srcline'),before ='' , element =self.sregex, after = '')     # requires application_1_4_7 or above
            
            # search all patterns in current program
            try:
#                 self.propvalue =[]
                getvalue=""
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
                getvalue=str(cntprop)
                #logging.debug("Value of list-->"+ str(getvalue))
                if cntprop >0:
                    file.save_property('dboraclemigrationScript.'+sobjname, getvalue)
                    logging.debug("property saved: --->" +'dboraclemigrationScript.'+sobjname +" "+getvalue)
               
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

                #end
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Built_in_SQL_Functions_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.SQL_language_elements_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Datetime_interval_expressions_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.Data_Types_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.SELECT_Statement_variations',[declareitems])
                application.declare_property_ownership('dboraclemigration_CustomMetrics.CREATE_TABLE_statement_variations',[declareitems])