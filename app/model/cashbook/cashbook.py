import MySQLdb
import datetime
from decimal import Decimal

from db import DBConnector
from model.project import project

class cashbook:
    """現金出納帳モデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["user_id"] = None
        self.attr["ym"] = None
        self.attr["date"] = None
        self.attr["summary"] = None
        self.attr["detail"] = None
        self.attr["income"] = None
        self.attr["expenses"] = None
        self.attr["amount"] = None
        self.attr["last_updated"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_cashbook;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_cashbook` (
                `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `user_id` int(11) unsigned NOT NULL,
                `ym` int(11) NOT NULL,
                `date` date NOT NULL,
                `summary` varchar(255) DEFAULT NULL,
                `detail` text,
                `income` decimal(12,0) NOT NULL DEFAULT '0',
                `expenses` decimal(12,0) NOT NULL DEFAULT '0',
                `amount` decimal(12,0) NOT NULL DEFAULT '0',
                `last_updated` datetime NOT NULL,
                PRIMARY KEY (`id`),
                KEY `user_id` (`user_id`),
                KEY `summary` (`summary`)
                )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_cashbook
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        cb = cashbook()
        cb.attr["id"] = data["id"]
        cb.attr["user_id"] = data["user_id"]
        cb.attr["ym"] = data["ym"]
        cb.attr["date"] = data["date"]
        cb.attr["summary"] = data["summary"]
        cb.attr["detail"] = data["detail"]
        cb.attr["income"] = data["income"]
        cb.attr["expenses"] = data["expenses"]
        cb.attr["amount"] = data["amount"]
        cb.attr["last_updated"] = data["last_updated"]
        return cb

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
          self.attr["ym"] is not None and type(self.attr["ym"]) is int and len(str(self.attr["ym"])) == 6,
          self.attr["date"] is not None and type(self.attr["date"]) is datetime.date,
          self.attr["summary"] is not None and type(self.attr["summary"]) is str and len(self.attr["summary"]) > 0,
          self.attr["detail"] is None or type(self.attr["detail"]) is str,
          self.attr["income"] is not None and type(self.attr["income"]) is Decimal,
          self.attr["expenses"] is not None and type(self.attr["expenses"]) is Decimal,
          self.attr["amount"] is not None and type(self.attr["amount"]) is Decimal and self.attr["amount"] == self.attr["income"] - self.attr["expenses"],
          self.attr["last_updated"] is not None and type(self.attr["last_updated"]) is datetime.datetime
        ])


    @staticmethod
    def build():
        now = datetime.datetime.now()
        cb = cashbook()
        # defaultが設定されている変数はdefault値にしておくと良い
        # 日付も予め値が入っていた方が良い
        # 入力が必要な物はNoneのままにしておく
        cb.attr["ym"] = now.year*100 + now.month
        cb.attr["date"] = now.date()
        #cb.attr["summary"] = None
        #cb.attr["detail"] = None
        cb.attr["income"] = Decimal(0)
        cb.attr["expenses"] = Decimal(0)
        cb.attr["amount"] = Decimal(0)
        cb.attr["last_updated"] = now
        return cb

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    def _db_save_insert(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_cashbook
                    (user_id, ym, date, summary, detail, income, expenses, amount, last_updated)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                (self.attr["user_id"],
                self.attr["ym"],
                self.attr["date"],
                self.attr["summary"],
                self.attr["detail"],
                self.attr["income"],
                self.attr["expenses"],
                self.attr["amount"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"])))
            
            # INSERTされたAUTO INCREMENT値を取得
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]
    
    def _db_save_update(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_cashbook
                SET user_id = %s,
                    ym = %s,
                    date = %s,
                    summary = %s,
                    detail = %s,
                    income = %s,
                    expenses = %s,
                    amount = %s,
                    last_updatedemail = %s
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["ym"],
                self.attr["date"],
                self.attr["summary"],
                self.attr["detail"],
                self.attr["income"],
                self.attr["expenses"],
                self.attr["amount"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"]),
                self.attr["id"]))
            con.commit()
        
        return self.attr["id"]

    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_cashbook
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()
        
        records = []
        for data in results:
            cb = cashbook()
            cb.attr["id"] = data["id"]
            cb.attr["user_id"] = data["user_id"]
            cb.attr["ym"] = data["ym"]
            cb.attr["date"] = data["date"]
            cb.attr["summary"] = data["summary"]
            cb.attr["detail"] = data["detail"]
            cb.attr["income"] = data["income"]
            cb.attr["expenses"] = data["expenses"]
            cb.attr["amount"] = data["amount"]
            cb.attr["last_updated"] = data["last_updated"]
            records.append(cb)

        return records
    
    def delete(self):
        if self.attr["id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_cashbook
                WHERE id = %s; """,
                (self.attr["id"],))
            con.commit()

        return self.attr["id"]
    
    @staticmethod
    def _index(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT id FROM table_cashbook
                WHERE user_id = %s; """,
                (user_id,))
            con.commit()
            recodes = cursor.fetchall()
        
        ids = [recode[0] for recode in recodes]
        return ids

    @staticmethod
    def summary(user_id, summary):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT id FROM table_cashbook
                WHERE `user_id` = %s and `summary` = %s; """,
                (user_id, summary))
            con.commit()
            recodes = cursor.fetchall()
        
        cb_list = [cashbook.find(recode[0]) for recode in recodes]
        return cb_list

    @staticmethod
    def ym(user_id, ym):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM table_cashbook
                WHERE user_id = %s and ym = %s
                ORDER BY `date` ASC; """,
                (user_id,ym,))
            con.commit()
            recodes = cursor.fetchall()

        cb_list2 = [cashbook.find(recode[0]) for recode in recodes]
        return cb_list2
