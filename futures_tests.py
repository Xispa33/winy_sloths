import os
import subprocess
from time import *
from datetime import *
import unittest

class TestFutures(unittest.TestCase):

    def test_compute_side(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    
    def test_open_long(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.test

    def test_close_long(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_open_short(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.test

    def test_close_short(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    

if __name__ == '__main__':
    unittest.main()
shell_command = subprocess.run("python3 ex.py", shell=True, capture_output=True)
print(shell_command.stdout.decode("utf-8").rstrip('\n'))