import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from controller.AuthenticationHandlers import LoginBaseHandler


class UserMyPageHandler(LoginBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/mypageUser")
            return

        # サインインアーティストの取得
        _id = tornado.escape.xhtml_escape(self.current_user)

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # データ取得
        result = user.find(int(_id))
        favorite_id = result.attr["favorite"]
        favorite_fan_class = result.attr["fan_class"]
        favorite_sex = result.attr["sex"]
        favorite_genre = result.attr["genre"]

        if favorite_fan_class == "":
            favorite_fan_class = '選択しない'
        elif favorite_fan_class == "under_twenty":
            favorite_fan_class = '~20'
        elif favorite_fan_class == "twenties":
            favorite_fan_class = '20~30'
        elif favorite_fan_class == "thirties":
            favorite_fan_class = '30~40'
        elif favorite_fan_class == "forties":
            favorite_fan_class = '40~50'
        elif favorite_fan_class == "fifties":
            favorite_fan_class = '50~60'
        elif favorite_fan_class == "over_seventy":
            favorite_fan_class = '70~'

        if favorite_sex == "":
            favorite_sex = '選択しない'
        elif favorite_sex == "male":
            favorite_sex = '男'
        elif favorite_sex == "female":
            favorite_sex = '女'

        if favorite_genre == "":
            favorite_genre = '選択しない'
        elif favorite_genre == "pop":
            favorite_genre = 'POP'
        elif favorite_genre == "dance":
            favorite_genre = 'ダンス'
        elif favorite_genre == "animation":
            favorite_genre = 'アニメ'
        elif favorite_genre == "jazz":
            favorite_genre = 'ジャズ'
        elif favorite_genre == "reggae":
            favorite_genre = 'レゲエ'
        elif favorite_genre == "rbsoul":
            favorite_genre = 'R&Bソウル'
        elif favorite_genre == "classicalMusic":
            favorite_genre = 'クラシック'
        elif favorite_genre == "electronicMusic":
            favorite_genre = 'エレクトロニック'
        elif favorite_genre == "rock":
            favorite_genre = 'ロック'
        elif favorite_genre == "world":
            favorite_genre = 'ワールド'
        elif favorite_genre == "alternative":
            favorite_genre = 'オルタナティブ'
        elif favorite_genre == "popularSong":
            favorite_genre = '歌謡曲'
        elif favorite_genre == "blues":
            favorite_genre = 'ブルース'
        elif favorite_genre == "hiphopRap":
            favorite_genre = 'ヒップホップ＆ラップ'

        if favorite_id == 0:
            self.render("mypageUser.html", user=result,
                        favorite_artist_name='未登録',
                        favorite_fan_class='未登録',
                        favorite_sex='未登録',
                        favorite_genre='未登録',
                        messages=messages, errors=[])
        else:
            favorite_artist = user.find(favorite_id)
            self.render("mypageUser.html", user=result,
                        favorite_artist_name=favorite_artist.attr["artist_name"],
                        favorite_fan_class=favorite_fan_class,
                        favorite_sex=favorite_sex,
                        favorite_genre=favorite_genre,
                        messages=messages, errors=[])


class ArtistMyPageHandler(LoginBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/mypageArtist")
            return

        # サインインアーティストの取得
        _id = tornado.escape.xhtml_escape(self.current_user)

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # データ取得
        result = user.find(int(_id))
        _fan_class = result.attr["fan_class"]
        _sex = result.attr["sex"]
        _genre = result.attr["genre"]

        if _fan_class == "":
            _fan_class = '選択していない'
        elif _fan_class == "under_twenty":
            _fan_class = '~20'
        elif _fan_class == "twenties":
            _fan_class = '20~30'
        elif _fan_class == "thirties":
            _fan_class = '30~40'
        elif _fan_class == "forties":
            _fan_class = '40~50'
        elif _fan_class == "fifties":
            _fan_class = '50~60'
        elif _fan_class == "over_seventy":
            _fan_class = '70~'

        if _sex == "":
            _sex = '選択していない'
        elif _sex == "male":
            _sex = '男'
        elif _sex == "female":
            _sex = '女'

        if _genre == "":
            _genre = '選択していない'
        elif _genre == "pop":
            _genre = 'POP'
        elif _genre == "dance":
            _genre = 'ダンス'
        elif _genre == "animation":
            _genre = 'アニメ'
        elif _genre == "jazz":
            _genre = 'ジャズ'
        elif _genre == "reggae":
            _genre = 'レゲエ'
        elif _genre == "rbsoul":
            _genre = 'R&Bソウル'
        elif _genre == "classicalMusic":
            _genre = 'クラシック'
        elif _genre == "electronicMusic":
            _genre = 'エレクトロニック'
        elif _genre == "rock":
            _genre = 'ロック'
        elif _genre == "world":
            _genre = 'ワールド'
        elif _genre == "alternative":
            _genre = 'オルタナティブ'
        elif _genre == "popularSong":
            _genre = '歌謡曲'
        elif _genre == "blues":
            _genre = 'ブルース'
        elif _genre == "hiphopRap":
            _genre = 'ヒップホップ＆ラップ'

        self.render("mypageArtist.html", user=result,
                    fan_class=_fan_class,
                    sex=_sex,
                    genre=_genre,
                    messages=messages, errors=[])
