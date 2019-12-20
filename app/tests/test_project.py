import unittest
from model.project import project

class test_project(unittest.TestCase):
    def test_it_has_a_name(self):
        self.assertTrue(type(project.name()) == str)
        self.assertTrue(len(project.name()) > 0)