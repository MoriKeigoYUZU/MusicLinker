import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.cashbook import cashbook
from controller.AuthenticationHandlers import SigninBaseHandler

# class CashbooksHandler(SigninBaseHandler):
#     def get(self):
#         if not self.current_user:
#             self.redirect("/signin")
#             return
#         # サインインユーザーの取得
#         _id = tornado.escape.xhtml_escape(self.current_user)
#         _signedInUser = user.find(int(_id))

#         # 他の画面からのメッセージを取得
#         _message = self.get_argument("message", None)
#         messages = []
#         if _message is not None: messages.append(_message)

#         # ユーザーごとの現金出納帳データを取得
#         results = cashbook.select_by_user_id(_signedInUser.attr["id"])
#         self.render("cashbooks.html", user=_signedInUser, cashbooks=results, messages=messages, errors=[])
class CashbooksHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None: messages.append(_message)

        _summary= self.get_argument("summary", None)
        _ym = self.get_argument("ym", None)

        # ユーザーごとの現金出納帳データを取得
        if _ym is not None:
            results = cashbook.ym(_id,_ym)
        else:
            results = cashbook.select_by_user_id(_signedInUser.attr["id"])
        if _summary is not None:
            results = cashbook.summary(_id, _summary)
        else:
            results = cashbook.select_by_user_id(_signedInUser.attr["id"])

        self.render("cashbooks.html",
            user=_signedInUser,
            cashbooks=results,
            messages=messages,
            summary=_summary,
            errors=[])



class CashbookShowHandler(SigninBaseHandler):
    def get(self, id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        cb = cashbook.find(id)
        if cb is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        if cb.attr["user_id"] != _signedInUser.attr["id"]: raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        self.render("cashbook_form.html", user=_signedInUser, mode="show", cashbook=cb, messages=[], errors=[])

class CashbookCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        cb = cashbook.build()
        self.render("cashbook_form.html", user=_signedInUser, mode="new", cashbook=cb, messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_date = self.get_argument("form-date", None)
        p_summary = self.get_argument("form-summary", None)
        p_detail = self.get_argument("form-detail", None)
        p_income = self.get_argument("form-income", None)
        p_expenses = self.get_argument("form-expenses", None)

        # 現金出納帳データの組み立て
        cb = cashbook.build()
        cb.attr["user_id"] = int(_id) # ユーザーIDはサインインユーザーより取得

        # パラメータエラーチェック
        errors = []
        if p_date is None:
            errors.append("日付は必須です。")
        else:
            # 文字列をdatetime.dateオブジェクトへをキャスト
            cb.attr["date"] = datetime.datetime.strptime(p_date, '%Y-%m-%d').date()
            # 年月計算
            cb.attr["ym"] = cb.attr["date"].year * 100 + cb.attr["date"].month
        
        if p_summary is None: errors.append("摘要は必須です。")
        cb.attr["summary"] = p_summary
        cb.attr["detail"] = p_detail

        if p_income is None and p_expenses is None: errors.append("収入/支出のどちらかは入力してください。")
        if p_income is None: p_income = 0
        if p_expenses is None: p_expenses = 0
        cb.attr["income"] = Decimal(p_income)
        cb.attr["expenses"] = Decimal(p_expenses)
        # 金額計算(収入 - 支出)
        cb.attr["amount"] = cb.attr["income"] - cb.attr["expenses"]

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("cashbook_form.html", user=_signedInUser, mode="new", cashbook=cb, messages=[], errors=[])
            return
        
        # 登録
        # print(vars(cb))
        cb_id = cb.save()
        if cb_id == False:
            self.render("cashbook_form.html", user=_signedInUser, mode="new", cashbook=cb, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/cashbooks?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % cb_id))
