import unittest
import copy
from unittest import mock
from model.project_artist import project
from model.artist import artist


class test_user(unittest.TestCase):

    def setUp(self):
        self.a = artist()
        self.a.attr["artist_name"] = "爆弾ジョニー"
        self.a.attr["genre"] = "rock"
        self.a.attr["fan_class"] = "twenties"
        self.a.attr["password"] = "1234abc"
        self.patcher = mock.patch(
            'model.project_artist.project.name', return_value="test_artist")
        self.mock_name = self.patcher.start()
        artist.migrate()
        self.a.save()

    def tearDown(self):
        artist.db_cleaner()
        self.patcher.stop()

    def test_db_is_working(self):
        a = artist.find(self.a.attr["id"])
        self.assertTrue(type(a) is artist)
        self.assertTrue(a.attr["id"] == 1)

    # attrが正しい値を持っている

    def test_is_valid(self):
        self.assertTrue(self.a.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):

        # id : None or int
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["id"] = None
        self.assertTrue(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["id"] = "1"
        self.assertFalse(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["id"] = 1
        self.assertTrue(artist_wrong.is_valid())

        # artist_name : not None and str
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["artist_name"] = None
        self.assertFalse(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["artist_name"] = "yukipi"
        self.assertTrue(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["artist_name"] = 1
        self.assertFalse(artist_wrong.is_valid())

        # genre : not None and str
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["genre"] = None
        self.assertFalse(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["genre"] = "yukipi"
        self.assertTrue(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["genre"] = 1
        self.assertFalse(artist_wrong.is_valid())

        # fan_class : not None and str
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["fan_class"] = None
        self.assertFalse(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["fan_class"] = "yukipi"
        self.assertTrue(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["fan_class"] = 1
        self.assertFalse(artist_wrong.is_valid())

        # password : not None and str
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["password"] = None
        self.assertFalse(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["password"] = "yukipi"
        self.assertTrue(artist_wrong.is_valid())
        artist_wrong = copy.deepcopy(self.a)
        artist_wrong.attr["password"] = 1
        self.assertFalse(artist_wrong.is_valid())

    def test_save_INSERT(self):
        a = artist()
        a.attr["artist_name"] = "爆弾ジョニー"
        a.attr["genre"] = "rock"
        a.attr["fan_class"] = "twenties"
        a.attr["password"] = "1234abc"
        result = a.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(a.attr["id"] is not None)
        self.assertTrue(a.attr["artist_name"] is not None)
        self.assertTrue(a.attr["genre"] is not None)
        self.assertTrue(a.attr["fan_class"] is not None)
        self.assertTrue(a.attr["password"] is not None)

    def test_save_UPDATE(self):
        a = artist()
        a.attr["id"] = 1
        a.attr["artist_name"] = "ONIGAWARA"
        a.attr["genre"] = "pop"
        a.attr["fan_class"] = "thirties"
        a.attr["password"] = "abc1234"
        result = a.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(a.attr["id"] is not None)
        self.assertTrue(a.attr["artist_name"] is not None)
        self.assertTrue(a.attr["genre"] is not None)
        self.assertTrue(a.attr["fan_class"] is not None)
        self.assertTrue(a.attr["password"] is not None)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
