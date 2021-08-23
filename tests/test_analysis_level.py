import os
import unittest
from cast.analysers.test import UATestAnalysis



class Test(unittest.TestCase):
    
    def testName(self):
        print (os.getcwd())
        analysis = UATestAnalysis('oracleToMySqlmigration')
#         analysis.add_selection("0.9")
        analysis.add_selection("oracleToMySqlmigration")
        analysis.set_verbose()
        analysis.run()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()