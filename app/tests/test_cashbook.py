import unittest
import datetime
import copy
from model.project import project
from model.cashbook import cashbook
from unittest import mock
from decimal import Decimal

# テスト途中で止めたい時は次の行を挿入する
# import pdb; pdb.set_trace()

class test_cashbook(unittest.TestCase):

    def setUp(self):
        # テストで使うcashbookを1つ作成
        # 正しい値を持ったインスタンスを作成しデータベースに登録まで行う
        self.cb = cashbook()
        self.cb.attr["user_id"] = 2
        self.cb.attr["ym"] = 201911
        self.cb.attr["date"] = datetime.datetime.now().date()
        self.cb.attr["summary"] = "バイト賃金"
        self.cb.attr["detail"] = "11月のバイト賃金"
        self.cb.attr["income"] = Decimal(20000)
        self.cb.attr["expenses"] = Decimal(0)
        self.cb.attr["amount"] = Decimal(20000)
        self.cb.attr["last_updated"] = datetime.datetime.now()

        # project.nameを書き換えておくことでテスト用のDBを利用する
        self.patcher = mock.patch('model.project.project.name', return_value="test_cashbook")
        self.mock_name = self.patcher.start()
        cashbook.migrate()
        self.cb.save()

    def tearDown(self):
        # テストが終わるたびにテスト用DBをクリア
        cashbook.db_cleaner()
        self.patcher.stop()
        
    def test_db_is_working(self):
        cb = cashbook.find(self.cb.attr["id"])
        # findで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(cb) is cashbook)
        # 最初のheroなのでidは1になる
        self.assertTrue(cb.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.cb.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invalid_attrs(self):
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["user_id"] = None # user_id must be a int
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["ym"] = 1911 # ym must be a int and its length must be 6
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["date"] = 12345 # date must be a datatime.date object
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["summary"] = 12345 # summary must be a sting
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["detail"] = None # detail must be None or a string
        self.assertTrue(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["detail"] = 12345 # detail must be None or a string
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["income"] = 12345 # income must be a Desimal
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["expenses"] = 12345 # expansed must be a Desimal
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["amount"] = Decimal(-20000) #amount must be equal to income + expamses
        self.assertFalse(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.cb)
        cb_wrong.attr["last_updated"] = None # last_updated must be a datetime.datetime object
        self.assertFalse(cb_wrong.is_valid())

    # default値を持ったcashbookインスタンスを生成する
    # Controlerで入力フォームを作るのにも利用する
    def test_build(self):
        cb = cashbook.build()
        self.assertTrue(type(cb) is cashbook)

    # save関数のテストを行う
    # 正例だけ出なく負例もテストするとなお良い
    def test_save(self):
        cb = cashbook.build()
        cb.attr["user_id"] = 2
        cb.attr["summary"] = "テスト"
        cb.attr["detail"] = None
        cb.attr["income"] += 10000
        cb.attr["expenses"] += 5000
        cb.attr["amount"] += 5000
        cb_id = cb.save()
        #import pdb; pdb.set_trace()
        self.assertTrue(type(cb_id) is int)
        self.assertTrue(cb.attr["id"] is not None)
        self.assertTrue(cb_id == cb.attr["id"])
        self.assertTrue(cb_id == 2)

    def test__index(self):
        self.assertEqual(len(cashbook._index(2)), 1)
        self.assertEqual(cashbook._index(2)[0], 1)

    def test_summary(self):
        user_id = 2
        summary = '光熱費'

        cb1 = cashbook.build()
        cb1.attr["user_id"] = user_id
        cb1.attr["date"] = '2019-10-31'
        cb1.attr["summary"] = summary
        cb1.attr["detail"] = None
        cb1.attr["income"] += 0
        cb1.attr["expenses"] += 7000
        cb1.attr["amount"] += -7000
        cb1_id = cb1.save()

        cb2 = cashbook.build()
        cb2.attr["user_id"] = user_id
        cb2.attr["date"] = '2019-11-30'
        cb2.attr["summary"] = summary
        cb2.attr["detail"] = None
        cb2.attr["income"] += 0
        cb2.attr["expenses"] += 5000
        cb2.attr["amount"] += -5000
        cb2_id = cb2.save()
        cb_list = cashbook.summary(user_id, summary)
        self.assertEqual(len(cb_list), 2)
        self.assertTrue(type(cb_list[0]) is cashbook)
        self.assertTrue(cb_list[0].attr['date'] < cb_list[1].attr['date'])
        
    def test_ym(self):
        user_id = 3
        ym = 201910
        ym2 = 201911

        cb1 = cashbook.build()
        cb1.attr["user_id"] = user_id
        cb1.attr["ym"] = ym
        cb1.attr["date"] = '2019-10-31'
        cb1.attr["summary"] = '光熱費'
        cb1.attr["detail"] = None
        cb1.attr["income"] += 0
        cb1.attr["expenses"] += 7000
        cb1.attr["amount"] += -7000
        cb1_id = cb1.save()

        cb2 = cashbook.build()
        cb2.attr["user_id"] = user_id
        cb2.attr["ym"] = ym
        cb2.attr["date"] = '2019-10-30'
        cb2.attr["summary"] = '家電'
        cb2.attr["detail"] = None
        cb2.attr["income"] += 0
        cb2.attr["expenses"] += 400000
        cb2.attr["amount"] += -400000
        cb2_id = cb2.save()

        #2019年10月の集計
        cb_list = cashbook.ym(user_id, ym)

        cb3 = cashbook.build()
        cb3.attr["user_id"] = user_id
        cb3.attr["ym"] = ym2
        cb3.attr["date"] = '2019-11-30'
        cb3.attr["summary"] = '光熱費'
        cb3.attr["detail"] = None
        cb3.attr["income"] += 0
        cb3.attr["expenses"] += 7000
        cb3.attr["amount"] += -7000
        cb3_id = cb3.save()

        cb4 = cashbook.build()
        cb4.attr["user_id"] = user_id
        cb4.attr["ym"] = ym2
        cb4.attr["date"] = '2019-11-13'
        cb4.attr["summary"] = '家電'
        cb4.attr["detail"] = None
        cb4.attr["income"] += 0
        cb4.attr["expenses"] += 400000
        cb4.attr["amount"] += -400000
        cb4_id = cb4.save()

        #2019年11月の集計
        cb_list2 = cashbook.ym(user_id, ym2)
        
        self.assertEqual(len(cb_list), 2)
        self.assertTrue(type(cb_list[0]) is cashbook)
        self.assertTrue(cb_list[0].attr['date'] < cb_list[1].attr['date'])
        self.assertEqual(len(cb_list2), 2)
        self.assertTrue(type(cb_list2[0]) is cashbook)
        self.assertTrue(cb_list2[0].attr['date'] < cb_list2[1].attr['date'])
        self.assertTrue(type(cb1.attr["ym"]) is int)  #cb1.attr["ym"]はint型
        self.assertTrue(type(cb2.attr["ym"]) is int)  #cb2.attr["ym"]はint型
        self.assertTrue(type(cb3.attr["ym"]) is int)  #cb3.attr["ym"]はint型
        self.assertTrue(type(cb4.attr["ym"]) is int)  #cb4.attr["ym"]はint型
        self.assertEqual(len(str(cb1.attr["ym"])), 6)  #cb1.attr["ym"]は6桁
        self.assertEqual(len(str(cb2.attr["ym"])), 6)  #cb2.attr["ym"]は6桁
        self.assertEqual(len(str(cb3.attr["ym"])), 6)  #cb3.attr["ym"]は6桁
        self.assertEqual(len(str(cb4.attr["ym"])), 6)  #cb4.attr["ym"]は6桁
        
    
if __name__ == '__main__':
    # unittestを実行
    unittest.main()