import MySQLdb

from db import DBConnector
from model.project import project


class user:
    """ ユーザーモデル """

    def __init__(self):
        self.attr = {}
        # 共通
        self.attr["id"] = None
        self.attr["email"] = None
        # アーティストのみ
        self.attr["genre"] = None
        self.attr["sex"] = None
        self.attr["fan_class"] = None
        self.attr["artist_name"] = None
        # サポーターのみ
        self.attr["favorite"] = None
        # 共通
        self.attr["password"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' %
                           project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_user;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_user` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `email` varchar(255) NOT NULL DEFAULT '',
                    `genre` varchar(255) DEFAULT '',
                    `sex` varchar(255) DEFAULT '',
                    `fan_class` varchar(255) DEFAULT '',
                    `artist_name` varchar(255) DEFAULT '',
                    `favorite` int(11) DEFAULT 0,
                    `password` varchar(255) NOT NULL DEFAULT '',
                    PRIMARY KEY (`id`)
                ); """)
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
                FROM   table_user
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None

        data = results[0]
        u = user()
        u.attr["id"] = data["id"]
        u.attr["email"] = data["email"]
        u.attr["genre"] = data["genre"]
        u.attr["sex"] = data["sex"]
        u.attr["fan_class"] = data["fan_class"]
        u.attr["artist_name"] = data["artist_name"]
        u.attr["favorite"] = data["favorite"]
        u.attr["password"] = data["password"]
        return u

    def is_valid(self):
        return all([
            self.attr["id"] is None or type(self.attr["id"]) is int,
            self.attr["email"] is not None and type(self.attr["email"]) is str,
            self.attr["genre"] is None or type(self.attr["genre"]) is str,
            self.attr["sex"] is None or type(self.attr["sex"]) is str,
            self.attr["fan_class"] is None or type(
                self.attr["fan_class"]) is str,
            self.attr["artist_name"] is None or type(
                self.attr["artist_name"]) is str,
            self.attr["favorite"] is None or type(
                self.attr["favorite"]) is int,
            self.attr["password"] is not None and type(
                self.attr["password"]) is str,
        ])

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
                INSERT INTO table_user
                    (email, genre, sex, fan_class, artist_name, favorite, password)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s); """,
                           (self.attr["email"],
                            self.attr["genre"],
                            self.attr["sex"],
                            self.attr["fan_class"],
                            self.attr["artist_name"],
                            self.attr["favorite"],
                            self.attr["password"]))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_user
                SET email = %s,
                    genre = %s,
                    sex = %s,
                    fan_class = %s,
                    artist_name = %s,
                    favorite = %s,
                    password = %s
                WHERE id = %s; """,
                           (self.attr["email"],
                            self.attr["genre"],
                            self.attr["sex"],
                            self.attr["fan_class"],
                            self.attr["artist_name"],
                            self.attr["favorite"],
                            self.attr["password"],
                            self.attr["id"]))

            con.commit()

        return self.attr["id"]

    # サポーターとユーザーを識別
    def mode_identification(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            if self.attr["artist_name"] == None:
                return all([
                    self.attr["id"] is None or type(self.attr["id"]) is int,
                    self.attr["email"] is not None and type(
                        self.attr["email"]) is str,
                    self.attr["favorite"] is None or type(
                        self.attr["favorite"]) is int,
                    self.attr["password"] is not None and type(
                        self.attr["password"]) is str,
                ])
            return all([
                self.attr["id"] is None or type(self.attr["id"]) is int,
                self.attr["email"] is not None and type(
                    self.attr["email"]) is str,
                self.attr["genre"] is None or type(self.attr["genre"]) is str,
                self.attr["sex"] is None or type(self.attr["sex"]) is str,
                self.attr["fan_class"] is None or type(
                    self.attr["fan_class"]) is str,
                self.attr["artist_name"] is None or type(
                    self.attr["artist_name"]) is str,
                self.attr["password"] is not None and type(
                    self.attr["password"]) is str,
            ])

    # favorite更新
    def favorite_update(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_user
                SET favorite = %s 
                WHERE id = %s; """,
                           (self.attr["favorite"],
                            self.attr["id"]))

            con.commit()

        return self.attr["id"]

    # search機構
    # 展望 : できればお気に入り登録の多い順に並べたいよねっていう気持ち　''' ORDER BY '''
    @staticmethod
    def search_artists(genre, sex, fan_class):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # sql文を条件によってtxtデータにする
            sql_select = "SELECT * FROM table_user"

            if genre is not None:
                sql_select += " WHERE genre = '" + genre + "'"
                if sex is not None:
                    sql_select += " AND sex = '" + sex + "'"
                if fan_class is not None:
                    sql_select += " AND fan_class = '" + fan_class + "'"
            elif sex is not None:
                sql_select += " WHERE sex = '" + sex + "'"
                if fan_class is not None:
                    sql_select += " AND fan_class = '" + fan_class + "'"
            elif fan_class is not None:
                sql_select += " WHERE fan_class = '" + fan_class + "'"

            cursor.execute(sql_select)
            con.commit()
            recodes = cursor.fetchall()

            u_list = [user.find(recode[0]) for recode in recodes]
            return u_list
