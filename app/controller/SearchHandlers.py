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

        results = user.search_artists(_genre, _sex, _fan_class)

        print(type(results))
        print(len(results))
        print(_genre)
        print(_sex)
        print(_fan_class)

        self.render("searchResults.html",
                    user=_signedInUser,
                    artists=results,
                    messages=messages,
                    errors=[])

        # self.redirect("/searchResults",
        #               user=_signedInUser,
        #               artists=results,
        #               messages=messages,
        #               errors=[])


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

        result = _signedInUser.favorite_update()

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
