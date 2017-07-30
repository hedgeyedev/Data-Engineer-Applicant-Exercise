import unittest
from template import template
 
#I initialized the variables in the class instead so they can be reused
 
class TestTemplate(unittest.TestCase):
    
    def setUp(self):
        self.start = 5 #start of string
        self.end = 8 #end of string
        self.code = "%CODE%"
        self.altcode = "%ALTCODE%"
    
 
    def test_substitute_code_and_altcode(self):
        self.assertEqual( template('Code is %CODE%; alt code is %ALTCODE%', '5678901234', self.start, self.end, self.code, self.altcode), 'Code is 5678901234; alt code is 56789-012')
 
 
if __name__ == '__main__':
    unittest.main()
