import tornado.web
import json
from model.user import user
from controller.AuthenticationHandlers import LoginBaseHandler
class TopHandler(LoginBaseHandler):
    def get(self):
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("top.html", errors=[], messages=messages)
class SearchHandler(LoginBaseHandler):
    def get(self):
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("search.html", errors=[], messages=messages)
    def post(self):
        # サインインユーザの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        # 概要を取得
        _genre = self.get_argument("sound", None)
        _sex = self.get_argument("sex", None)
        _fan_class = self.get_argument("age", None)
        if len(_genre) | len(_sex) | len(_fan_class):
            results = user.search_artists(_genre, _sex, _fan_class)
        else:
            results = user.artist_all()
        artist_name_list = []
        genre_list = []
        sex_list = []
        fan_class_list = []
        for result in results:
            artist_name_list.append(result.attr["artist_name"])
            if result.attr["fan_class"] == "under_twenty":
                fan_class_list.append('~20')
            elif result.attr["fan_class"] == "twenties":
                fan_class_list.append('20~30')
            elif result.attr["fan_class"] == "thirties":
                fan_class_list.append('30~40')
            elif result.attr["fan_class"] == "forties":
                fan_class_list.append('40~50')
            elif result.attr["fan_class"] == "fifties":
                fan_class_list.append('50~60')
            elif result.attr["fan_class"] == "over_seventy":
                fan_class_list.append('70~')
            if result.attr["sex"] == "male":
                sex_list.append('男')
            elif result.attr["sex"] == "female":
                sex_list.append('女')
            if result.attr["genre"] == "pop":
                genre_list.append('POP')
            elif result.attr["genre"] == "dance":
                genre_list.append('ダンス')
            elif result.attr["genre"] == "animation":
                genre_list.append('アニメ')
            elif result.attr["genre"] == "jazz":
                genre_list.append('ジャズ')
            elif result.attr["genre"] == "reggae":
                genre_list.append('レゲエ')
            elif result.attr["genre"] == "rbsoul":
                genre_list.append('R&Bソウル')
            elif result.attr["genre"] == "classicalMusic":
                genre_list.append('クラシック')
            elif result.attr["genre"] == "electronicMusic":
                genre_list.append('エレクトロニック')
            elif result.attr["genre"] == "rock":
                genre_list.append('ロック')
            elif result.attr["genre"] == "world":
                genre_list.append('ワールド')
            elif result.attr["genre"] == "alternative":
                genre_list.append('オルタナティブ')
            elif result.attr["genre"] == "popularSong":
                genre_list.append('歌謡曲')
            elif result.attr["genre"] == "blues":
                genre_list.append('ブルース')
            elif result.attr["genre"] == "hiphopRap":
                genre_list.append('ヒップホップ＆ラップ')
        print(type(results))
        print(len(results))
        print(_genre)
        print(_sex)
        print(_fan_class)
        self.render("searchResults.html",
                    user=_signedInUser,
                    artists=results,
                    artist_name_list=artist_name_list,
                    fan_class_list=fan_class_list,
                    sex_list=sex_list,
                    genre_list=genre_list,
                    messages=messages,
                    errors=[])
class SearchResultsHandler(LoginBaseHandler):
    def get(self):
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("searchResults.html", errors=[], messages=messages)
    def post(self):
        # サインインユーザの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        # 概要を取得
        _favorite_id = self.get_argument("favorite", None)
        result = _signedInUser.favorite_update(_favorite_id, _id)
        if result is None:
            self.redirect("/mypageUser")
        else:
            if result == False:
                self.render("serarchResults.html",
                            user=_signedInUser,
                            artists=result,
                            messages=[],
                            errors=["できませーん"])
            else:
                self.redirect("/mypageUser?message=%s" %
                              tornado.escape.url_escape("お気に入り登録完了"))