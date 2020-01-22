import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from controller.AuthenticationHandlers import LoginBaseHandler


class UserMyPageHandler(LoginBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/mypageUser")  # ここ飛び先
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
        favorite_artist = user.find(favorite_id)
        # favorite_fan_class = result.attr["fan_class"]
        # favorite_genre = result.attr["genre"]
        # favorite_sex = result.attr["sex"]

        if favorite_id == 0:
            # print("hoge111111111111111")
            # self.render("mypageUser.html", user=result, favorite_artist_name='未登録',
            #             messages=messages, errors=[])
            self.render("mypageUser.html", user=result, favorite_artist=favorite_artist,
                        messages=messages, errors=[])
        else:
            # print("hoge22222222222222")
            favorite_artist = user.find(favorite_id)
            # self.render("mypageUser.html", user=result,
            #             favorite_artist_name=favorite_artist.attr["artist_name"], messages=messages, errors=[])
            self.render("mypageUser.html", user=result, favorite_artist=favorite_artist,
                        messages=messages, errors=[])


class ArtistMyPageHandler(LoginBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/mypageArtist")  # ここ飛び先
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

        _fan_class = result.attr
        self.render("mypageArtist.html", user=result,
                    messages=messages, errors=[])
