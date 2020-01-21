import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from controller.AuthenticationHandlers import LoginBaseHandler


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
        results = user.find(int(_id))
        self.render("mypageArtist.html", user=results,
                    messages=messages, errors=[])


# TODO
# 動作確認

class CashbookCreateHandler(LoginBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        art = user.find(int(_id))
        self.render("signupArtist.html", user=art,
                    mode="new", messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/login")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_artist_name = self.get_argument("artist_name", None)
        p_email = self.get_argument("username", None)
        p_password = self.get_argument("password", None)
        p_fan_class = self.get_argument("age", None)
        p_sex = self.get_argument("sex", None)
        p_genre = self.get_argument("sound", None)

        # アーティストデータの組み立て
        art = user.build()
        art.attr["user_id"] = int(_id)  # ユーザーIDはサインインユーザーより取得

        # パラメータエラーチェックと代入
        errors = []
        if p_artist_name is None:
            # ユーザーと判別
            p_artist_name = None
        # アーティストと判別
        art.attr["artist_name"] = p_artist_name

        if p_email is None:
            errors.append("メールアドレスは必須です。")
        art.attr["email"] = p_email

        if p_password is None:
            errors.append("パスワードは必須です。")
        art.attr["password"] = p_password

        if p_fan_class is None:
            errors.append("ファンの年齢層を入れてください。")
        art.attr["fan_class"] = Decimal(p_fan_class)

        if p_sex is None:
            errors.append("ファンの性別は必須です。")
        art.attr["sex"] = Decimal(p_sex)

        if p_genre is None:
            errors.append("音楽のジャンルは必須です。")
        art.attr["genre"] = p_genre

        if len(errors) > 0:  # エラーは新規登録画面に渡す
            self.render("signupArtist.html", user=art,
                        mode="new",  messages=[], errors=[])
            return

        # 登録
        # print(vars(art))
        art_id = art.save()
        if art_id == False:
            self.render("signupArtist.html", user=art, mode="new",
                        messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/signupArtist.html?message=%s" %
                          tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % art_id))
