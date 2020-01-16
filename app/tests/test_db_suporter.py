import unittest
import copy
from unittest import mock
from model.project import project
from model.user import user


class test_user(unittest.TestCase):

    def setUp(self):
        self.u = user()
        self.u.attr["email"] = "miwa@ushi.com"
        self.u.attr["favorite"] = 1
        self.u.attr["password"] = "1234abc"
        self.patcher = mock.patch(
            'model.project.project.name', return_value="test_db_artist")
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

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.u.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):

        # id : None or int
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["id"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["id"] = "1"
        self.assertFalse(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["id"] = 1
        self.assertTrue(user_wrong.is_valid())

        # email : not None and str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["email"] = None
        self.assertFalse(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["email"] = "yukipi@ushi.com"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["email"] = 1
        self.assertFalse(user_wrong.is_valid())

        # genre : None or str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["genre"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["genre"] = "yukipi"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["genre"] = 1
        self.assertFalse(user_wrong.is_valid())

        # sex : None or str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["sex"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["sex"] = "male"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["sex"] = 1
        self.assertFalse(user_wrong.is_valid())

        # fan_class : None or str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["fan_class"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["fan_class"] = "forties"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["fan_class"] = 1
        self.assertFalse(user_wrong.is_valid())

        # artist_name : None or str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["artist_name"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["artist_name"] = "yukipi"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["artist_name"] = 1
        self.assertFalse(user_wrong.is_valid())

        # favorite : None or int
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["favorite"] = None
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["favorite"] = "yukipi"
        self.assertFalse(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["favorite"] = 1
        self.assertTrue(user_wrong.is_valid())

        # password : not None and str
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["password"] = None
        self.assertFalse(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["password"] = "yukipi"
        self.assertTrue(user_wrong.is_valid())
        user_wrong = copy.deepcopy(self.u)
        user_wrong.attr["password"] = 1
        self.assertFalse(user_wrong.is_valid())

    def test_save_INSERT(self):
        u = user()
        u.attr["id"] = 2
        u.attr["email"] = "ushi@miwa.com"
        u.attr["genre"] = "pop"
        u.attr["sex"] = "female"
        u.attr["fan_class"] = "thirties"
        u.attr["artist_name"] = "ONIGAWARA"
        u.attr["password"] = "hijiri_san"
        result = u.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is not None)
        self.assertTrue(u.attr["sex"] is not None)
        self.assertTrue(u.attr["fan_class"] is not None)
        self.assertTrue(u.attr["artist_name"] is not None)
        self.assertTrue(u.attr["favorite"] is None)
        self.assertTrue(u.attr["password"] is not None)

    def test_save_UPDATE(self):
        u = user()
        u.attr["id"] = 1
        u.attr["email"] = "nannimo@nai.com"
        u.attr["genre"] = "alternative"
        u.attr["sex"] = "female"
        u.attr["fan_class"] = "twenties"
        u.attr["artist_name"] = "SAMURAIMANZGROOVE"
        u.attr["password"] = "tadahitori"
        result = u.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is not None)
        self.assertTrue(u.attr["sex"] is not None)
        self.assertTrue(u.attr["fan_class"] is not None)
        self.assertTrue(u.attr["artist_name"] is not None)
        self.assertTrue(u.attr["favorite"] is None)
        self.assertTrue(u.attr["password"] is not None)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
