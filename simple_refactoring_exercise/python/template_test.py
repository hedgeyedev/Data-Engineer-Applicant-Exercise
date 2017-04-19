import unittest
from template import template
 
class TestTemplate(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_substitute_code_and_altcode(self):
        self.assertEqual( template('Code is %CODE%; %CODE% alt code is %ALTCODE% %ALTCODE%', '5678901234'), 'Code is 5678901234; 5678901234 alt code is 56789-012 56789-012')
 
 
if __name__ == '__main__':
    unittest.main()