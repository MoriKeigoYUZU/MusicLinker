import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.user import user

class test_user(unittest.TestCase):

    def setUp(self):
        self.u = user.build()
        self.u.attr["email"] = "hoge@fuga.piyo"
        self.u.attr["name"] = "Hoge"
        self.u.attr["password"] = "hogehogefugafuga"
        self.patcher = mock.patch('model.project.project.name', return_value="test_user")
        self.mock_name = self.patcher.start()
        user.migrate()
        self.u.save()

    def tearDown(self):
        user.db_cleaner()
        self.patcher.stop()
        
    def test_db_is_working(self):
        u = user.find(self.u.attr["id"])
        self.assertTrue(type(u) is user)
        self.assertTrue(u.attr["id"] == 1)

    def test_find_by_email動作確認(self):
        u = user.find_by_email(self.u.attr["email"])
        self.assertTrue(type(u) is user)
        self.assertTrue(u.attr["id"] == 1)
        self.assertTrue(u.attr["email"] == self.u.attr["email"])

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.u.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):
        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["email"] = 12345 # email must be a sting
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["name"] = 12345 # name must be a sting
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["password"] = None # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["password"] = 12345 # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["last_updated"] = None # last_updated must be a datetime.datetime object
        self.assertFalse(cb_wrong.is_valid())

    def test_build(self):
        u = user.build()
        self.assertTrue(type(u) is user)

    def test_save_INSERT(self):
        u = user.build()
        u.attr["email"] = "hoge2@fuga.piyo"
        u.attr["name"] = "Hoge"
        u.attr["password"] = "HogeHogeFugaFuga"
        result = u.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)

    def test_save_UPDATE(self):
        u = user.build()
        u.attr["id"] = 1
        u.attr["email"] = "new_hoge@fuga.piyo"
        u.attr["name"] = "new_Hoge"
        u.attr["password"] = "new_HogeHogeFugaFuga"
        result = u.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()