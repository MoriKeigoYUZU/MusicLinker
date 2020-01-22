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
            _favorite_fan_class = '選択しない'
        elif favorite_fan_class == "under_twenty":
            _favorite_fan_class = '~20'
        elif favorite_fan_class == "twenties":
            _favorite_fan_class = '20~30'
        elif favorite_fan_class == "thirties":
            _favorite_fan_class = '30~40'
        elif favorite_fan_class == "forties":
            _favorite_fan_class = '40~50'
        elif favorite_fan_class == "fifties":
            _favorite_fan_class = '50~60'
        elif favorite_fan_class == "over_seventy":
            _favorite_fan_class = '70~'

        if favorite_sex == "":
            _favorite_sex = '選択しない'
        elif favorite_sex == "male":
            _favorite_sex = '男'
        elif favorite_sex == "female":
            _favorite_sex = '女'

        if favorite_genre == "":
            _favorite_genre = '選択しない'
        elif favorite_genre == "pop":
            _favorite_genre = 'POP'
        elif favorite_genre == "dance":
            _favorite_genre = 'ダンス'
        elif favorite_genre == "animation":
            _favorite_genre = 'アニメ'
        elif favorite_genre == "jazz":
            _favorite_genre = 'ジャズ'
        elif favorite_genre == "reggae":
            _favorite_genre = 'レゲエ'
        elif favorite_genre == "rbsoul":
            _favorite_genre = 'R&Bソウル'
        elif favorite_genre == "classicalMusic":
            _favorite_genre = 'クラシック'
        elif favorite_genre == "electronicMusic":
            _favorite_genre = 'エレクトロニック'
        elif favorite_genre == "rock":
            _favorite_genre = 'ロック'
        elif favorite_genre == "world":
            _favorite_genre = 'ワールド'
        elif favorite_genre == "alternative":
            _favorite_genre = 'オルタナティブ'
        elif favorite_genre == "popularSong":
            _favorite_genre = '歌謡曲'
        elif favorite_genre == "blues":
            _favorite_genre = 'ブルース'
        elif favorite_genre == "hiphopRap":
            _favorite_genre = 'ヒップホップ＆ラップ'

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
                        favorite_fan_class=_favorite_fan_class,
                        favorite_sex=_favorite_sex,
                        favorite_genre=_favorite_genre,
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
        fan_class = result.attr["fan_class"]
        sex = result.attr["sex"]
        genre = result.attr["genre"]

        if fan_class == "":
            _fan_class = '選択していない'
        elif fan_class == "under_twenty":
            _fan_class = '~20'
        elif fan_class == "twenties":
            _fan_class = '20~30'
        elif fan_class == "thirties":
            _fan_class = '30~40'
        elif fan_class == "forties":
            _fan_class = '40~50'
        elif fan_class == "fifties":
            _fan_class = '50~60'
        elif fan_class == "over_seventy":
            _fan_class = '70~'

        if sex == "":
            _sex = '選択していない'
        elif sex == "male":
            _sex = '男'
        elif sex == "female":
            _sex = '女'

        if _gnre == "":
            _genre = '選択していない'
        elif genre == "pop":
            _genre = 'POP'
        elif genre == "dance":
            _genre = 'ダンス'
        elif genre == "animation":
            _genre = 'アニメ'
        elif genre == "jazz":
            _genre = 'ジャズ'
        elif genre == "reggae":
            _genre = 'レゲエ'
        elif genre == "rbsoul":
            _genre = 'R&Bソウル'
        elif genre == "classicalMusic":
            _genre = 'クラシック'
        elif genre == "electronicMusic":
            _genre = 'エレクトロニック'
        elif genre == "rock":
            _genre = 'ロック'
        elif genre == "world":
            _genre = 'ワールド'
        elif genre == "alternative":
            _genre = 'オルタナティブ'
        elif genre == "popularSong":
            _genre = '歌謡曲'
        elif genre == "blues":
            _genre = 'ブルース'
        elif genre == "hiphopRap":
            _genre = 'ヒップホップ＆ラップ'

        self.render("mypageArtist.html", user=result,
                    fan_class=_fan_class,
                    sex=_sex,
                    genre=_genre,
                    messages=messages, errors=[])
