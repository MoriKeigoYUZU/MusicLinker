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
        u.attr["email"] = "ushi@miwa.com"
        u.attr["password"] = "hijiri_san"
        result = u.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is None)
        self.assertTrue(u.attr["sex"] is None)
        self.assertTrue(u.attr["fan_class"] is None)
        self.assertTrue(u.attr["artist_name"] is None)
        self.assertTrue(u.attr["favorite"] is None)
        self.assertTrue(u.attr["password"] is not None)

    def test_save_UPDATE(self):
        u = user()
        u.attr["email"] = "nannimo@nai.com"
        u.attr["password"] = "tadahitori"
        result = u.save()

        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is None)
        self.assertTrue(u.attr["sex"] is None)
        self.assertTrue(u.attr["fan_class"] is None)
        self.assertTrue(u.attr["artist_name"] is None)
        self.assertTrue(u.attr["favorite"] is None)
        self.assertTrue(u.attr["password"] is not None)

    def test_favorite_updata(self):

        # お気に入り登録したいアーティストのデータ
        u1 = user()
        u1.attr["id"] = 1
        u1.attr["email"] = "rock@artist.com"
        u1.attr["genre"] = "rock"
        u1.attr["sex"] = "female"
        u1.attr["fan_class"] = "twenties"
        u1.attr["artist_name"] = "爆弾ジョニー"
        u1.attr["favorite"] = None
        u1.attr["password"] = "1234abc"
        artist_1 = u1.save()

        # お気に入り登録をするサポーターのデータ
        u = user()
        u.attr["id"] = 2
        u.attr["email"] = "nannimo@nai.com"
        u.attr["password"] = "tadahitori"
        suporter_1 = u.save()

        u.attr["favorite"] = 1

        result = u.favorite_update()

        self.assertEqual(suporter_1, result)
        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is None)
        self.assertTrue(u.attr["sex"] is None)
        self.assertTrue(u.attr["fan_class"] is None)
        self.assertTrue(u.attr["artist_name"] is None)
        self.assertTrue(u.attr["favorite"] is not None)
        self.assertTrue(u.attr["password"] is not None)

        u.attr["favorite"] = 2
        result = u.favorite_update()

        self.assertEqual(suporter_1, result)
        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)
        self.assertTrue(u.attr["genre"] is None)
        self.assertTrue(u.attr["sex"] is None)
        self.assertTrue(u.attr["fan_class"] is None)
        self.assertTrue(u.attr["artist_name"] is None)
        self.assertTrue(u.attr["favorite"] is not None)
        self.assertTrue(u.attr["password"] is not None)

    def test_search_artists(self):

        genre = "rock"
        sex = "female"
        fan_class = "twenties"

        user.migrate()

        # 全一致のデータ
        u1 = user()
        u1.attr["email"] = "rock@artist.com"
        u1.attr["genre"] = "rock"
        u1.attr["sex"] = "female"
        u1.attr["fan_class"] = "twenties"
        u1.attr["artist_name"] = "爆弾ジョニー"
        u1.attr["favorite"] = None
        u1.attr["password"] = "1234abc"
        artist_1 = u1.save()
        # genre, sex 一致のデータ
        u2 = user()
        u2.attr["email"] = "ushi@miwa.com"
        u2.attr["genre"] = "rock"
        u2.attr["sex"] = "female"
        u2.attr["fan_class"] = "thirties"
        u2.attr["artist_name"] = "ONIGAWARA"
        u2.attr["favorite"] = None
        u2.attr["password"] = "hijiri_san"
        artist_2 = u2.save()
        # sex, fan_class 一致のデータ
        u3 = user()
        u3.attr["email"] = "nannimo@nai.com"
        u3.attr["genre"] = "alternative"
        u3.attr["sex"] = "female"
        u3.attr["fan_class"] = "twenties"
        u3.attr["artist_name"] = "SAMURAIMANZGROOVE"
        u3.attr["password"] = "tadahitori"
        artist_3 = u3.save()
        # genre, fan_class 一致のデータ
        u4 = user()
        u4.attr["email"] = "loveme@fender.com"
        u4.attr["genre"] = "rock"
        u4.attr["sex"] = "male"
        u4.attr["fan_class"] = "twenties"
        u4.attr["artist_name"] = "ビレッジマンズストア"
        u4.attr["password"] = "tadasiiyoake"
        artist_4 = u4.save()
        # genre 一致のデータ
        u5 = user()
        u5.attr["email"] = "iwanna@bea.com"
        u5.attr["genre"] = "rock"
        u5.attr["sex"] = "male"
        u5.attr["fan_class"] = "thirties"
        u5.attr["artist_name"] = "みそっかす"
        u5.attr["password"] = "yorunobakemono"
        artist_5 = u5.save()
        # sex 一致のデータ
        u6 = user()
        u6.attr["email"] = "little@cloud.com"
        u6.attr["genre"] = "alternative"
        u6.attr["sex"] = "female"
        u6.attr["fan_class"] = "forties"
        u6.attr["artist_name"] = "SOPHIA"
        u6.attr["password"] = "kuroitongari"
        artist_6 = u6.save()
        # fan_class 一致のデータ
        u7 = user()
        u7.attr["email"] = "cool@des.com"
        u7.attr["genre"] = "alternative"
        u7.attr["sex"] = "male"
        u7.attr["fan_class"] = "twenties"
        u7.attr["artist_name"] = "バックドロップシンデレラ"
        u7.attr["password"] = "zyakuson"
        artist_7 = u7.save()
        # 一個も一致しないデータ
        u8 = user()
        u8.attr["email"] = "kyoukan@dekinai.com"
        u8.attr["genre"] = "alternative"
        u8.attr["sex"] = "male"
        u8.attr["fan_class"] = "thirties"
        u8.attr["artist_name"] = "八十八ヶ所巡礼"
        u8.attr["password"] = "jovejove"
        artist_8 = u8.save()

        self.assertEqual(u1.attr["id"], 1)
        self.assertEqual(u2.attr["id"], 2)
        self.assertEqual(u3.attr["id"], 3)
        self.assertEqual(u4.attr["id"], 4)
        self.assertEqual(u5.attr["id"], 5)
        self.assertEqual(u6.attr["id"], 6)
        self.assertEqual(u7.attr["id"], 7)
        self.assertEqual(u8.attr["id"], 8)

        artist_list = user.search_artists(genre, sex, fan_class)
        self.assertEqual(len(artist_list), 1)
        self.assertTrue(type(artist_list[0]) is user)

        artist_list_gs = user.search_artists(genre, sex, None)
        self.assertEqual(len(artist_list_gs), 2)
        self.assertTrue(type(artist_list_gs[0]) is user)
        self.assertTrue(type(artist_list_gs[1]) is user)

        artist_list_sf = user.search_artists(None, sex, fan_class)
        self.assertEqual(len(artist_list_sf), 2)
        self.assertTrue(type(artist_list_sf[0]) is user)
        self.assertTrue(type(artist_list_sf[1]) is user)

        artist_list_gf = user.search_artists(genre, None, fan_class)
        self.assertEqual(len(artist_list_gf), 2)
        self.assertTrue(type(artist_list_gf[0]) is user)
        self.assertTrue(type(artist_list_gf[1]) is user)

        artist_list_g = user.search_artists(genre, None, None)
        self.assertEqual(len(artist_list_g), 4)
        self.assertTrue(type(artist_list_g[0]) is user)
        self.assertTrue(type(artist_list_g[1]) is user)
        self.assertTrue(type(artist_list_g[2]) is user)
        self.assertTrue(type(artist_list_g[3]) is user)

        artist_list_s = user.search_artists(None, sex, None)
        self.assertEqual(len(artist_list_s), 4)
        self.assertTrue(type(artist_list_s[0]) is user)
        self.assertTrue(type(artist_list_s[1]) is user)
        self.assertTrue(type(artist_list_s[2]) is user)
        self.assertTrue(type(artist_list_s[3]) is user)

        artist_list_f = user.search_artists(None, None, fan_class)
        self.assertEqual(len(artist_list_f), 4)
        self.assertTrue(type(artist_list_f[0]) is user)
        self.assertTrue(type(artist_list_f[1]) is user)
        self.assertTrue(type(artist_list_f[2]) is user)
        self.assertTrue(type(artist_list_f[3]) is user)

        artist_list_all = user.search_artists(None, None, None)
        self.assertEqual(len(artist_list_all), 8)
        self.assertTrue(type(artist_list_all[0]) is user)
        self.assertTrue(type(artist_list_all[1]) is user)
        self.assertTrue(type(artist_list_all[2]) is user)
        self.assertTrue(type(artist_list_all[3]) is user)
        self.assertTrue(type(artist_list_all[4]) is user)
        self.assertTrue(type(artist_list_all[5]) is user)
        self.assertTrue(type(artist_list_all[6]) is user)
        self.assertTrue(type(artist_list_all[7]) is user)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
