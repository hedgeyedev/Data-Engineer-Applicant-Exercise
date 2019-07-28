import unittest
from template import template, template_refactor
 
class TestTemplate(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_refactor_substitute_code_and_altcode(self):
        self.assertEqual( template_refactor('Code is %CODE%; alt code is %ALTCODE%', 
        									'%CODE%', 
        									'%ALTCODE%', 
        									'5678901234'), 
        									'Code is 5678901234; alt code is 56789-012')
 

    def test_substitute_code_and_altcode(self):
        self.assertEqual( template('Code is %CODE%; alt code is %ALTCODE%', '5678901234'), 
        							'Code is 5678901234; alt code is 56789-012')
 
 
if __name__ == '__main__':
    unittest.main()
