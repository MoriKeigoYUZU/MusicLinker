import tornado.web

#
import json
#

"""以下の部分に関しては model の詳細が決まるまでなんとも言えない
from model.user import user
from model.cashbook import cashbook
"""
from model.user import user
from controller.AuthenticationHandlers import SigninBaseHandler


class UserHandler(SigninBaseHandler):
    def get(self):
        # サインインユーザの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # 概要を取得
        _genre = self.get_argument("genre", None)
        _sex = self.get_argument("sex", None)
        _fan_class = self.get_argument("fan_class", None)

        results = user.search_artists(_genre, _sex, _fan_class)

        self.render("searchResults.html",
                    user=json.dumps(_signedInUser),
                    artists=results,
                    messages=messages,
                    errors=[])