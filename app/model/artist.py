import MySQLdb

from db_artist import ArtistDBConnector
from model.project_artist import project


class artist:
    """ アーティストモデル """

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["artist_name"] = None
        self.attr["genre"] = None
        self.attr["fan_class"] = None
        self.attr["password"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with ArtistDBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' %
                           project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_artist;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_artist` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `artist_name` varchar(255) NOT NULL DEFAULT '',
                    `genre` varchar(255) DEFAULT NULL DEFAULT '',
                    `fan_class` varchar(255) DEFAULT NULL DEFAULT '',
                    `password` varchar(255) DEFAULT NULL DEFAULT '',
                    PRIMARY KEY (`id`)
                ); """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with ArtistDBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id):
        with ArtistDBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_artist
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None

        data = results[0]
        a = artist()
        a.attr["id"] = data["id"]
        a.attr["artist_name"] = data["artist_name"]
        a.attr["genre"] = data["genre"]
        a.attr["fan_class"] = data["fan_class"]
        a.attr["password"] = data["password"]
        return a

    def is_valid(self):
        return all([
            self.attr["id"] is None or type(
                self.attr["id"]) is int,
            self.attr["artist_name"] is not None and type(
                self.attr["artist_name"]) is str,
            self.attr["genre"] is not None and type(self.attr["genre"]) is str,
            self.attr["fan_class"] is not None and type(
                self.attr["fan_class"]) is str,
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

        with ArtistDBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_artist
                    (artist_name, genre, fan_class, password)
                VALUES
                    (%s, %s, %s, %s); """,
                           (self.attr["artist_name"],
                            self.attr["genre"],
                            self.attr["fan_class"],
                            self.attr["password"]))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with ArtistDBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_artist
                SET artist_name = %s,
                    genre = %s,
                    fan_class = %s,
                    password = %s
                WHERE id = %s; """,
                           (self.attr["artist_name"],
                            self.attr["genre"],
                            self.attr["fan_class"],
                            self.attr["password"],
                            self.attr["id"]))

            con.commit()

        return self.attr["id"]
