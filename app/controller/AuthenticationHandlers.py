import tornado.web
import hashlib  # パスワード暗号化のためのライブラリ
from model.user import user


# 認証を必要とするページは、このクラスを継承する
class LoginBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


# サインイン
class LoginUserHandler(LoginBaseHandler):
    def get(self):
        # パラメータを取得(2つ目の引数は、取得できない場合の初期値を設定できます。)
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("login.html", errors=[], messages=messages)

    def post(self):
        # パラメータの取得
        _email = self.get_argument("email", None)
        _raw_pass = self.get_argument("password", None)

        # エラーメッセージの初期化
        errors = []

        # 入力項目の必須チェック
        if _email == None or _raw_pass == None:
            if _email == None:
                errors.append("Sign in ID(Email Address) is required.")
            if _raw_pass == None:
                errors.append("Password is required.")
            self.render("login.html", errors=errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # 認証(ユーザーが存在する & パスワードが一致する で認証OK)
        if u == None or _pass != u.attr["password"]:
            # 認証失敗
            errors.append(
                "Sorry, your ID(Email Address) or password cannot be recognized.")
            self.render("login.html", errors=errors, messages=[])
            return

        # DBに保管されたユーザーIDを文字列化して暗号化Cookieに格納
        self.set_secure_cookie("user", str(u.attr["id"]))
        # 認証が必要なページへリダイレクト
        self.redirect("/mypageUser")


# サインイン
class LoginArtistHandler(LoginBaseHandler):
    def get(self):
        # パラメータを取得(2つ目の引数は、取得できない場合の初期値を設定できます。)
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("loginArtist.html", errors=[], messages=messages)

    def post(self):
        # パラメータの取得
        _email = self.get_argument("email", None)
        _raw_pass = self.get_argument("password", None)
        print(_email)
        print(_raw_pass)

        # エラーメッセージの初期化
        errors = []

        # 入力項目の必須チェック
        if _email == None or _raw_pass == None:
            if _email == None:
                errors.append("Sign in ID(Email Address) is required.")
            if _raw_pass == None:
                errors.append("Password is required.")
            self.render("loginArtist.html", errors=errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # 認証(ユーザーが存在する & パスワードが一致する で認証OK)
        if u == None or _pass != u.attr["password"]:
            # 認証失敗
            errors.append(
                "Sorry, your ID(Email Address) or password cannot be recognized.")
            self.render("loginArtist.html", errors=errors, messages=[])
            return

        # DBに保管されたユーザーIDを文字列化して暗号化Cookieに格納
        self.set_secure_cookie("user", str(u.attr["id"]))
        # 認証が必要なページへリダイレクト
        self.redirect("/mypageArtist")


# サインアウト
class SignoutHandler(LoginBaseHandler):
    def get(self):
        # 認証済みの暗号化Cookieを削除
        self.clear_cookie("user")
        # サインイン画面へリダイレクト(サインアウト完了の旨を添えて)
        self.redirect("/login?message=%s" %
                      tornado.escape.url_escape("You are now signed out."))


# サインアップ User
class SignupUserHandler(LoginBaseHandler):
    def get(self):
        # サインイン画面の表示
        self.render("signupUser.html", errors=[], messages=[])

    def post(self):
        # パラメータの取得
        _email = self.get_argument("email", None)
        _raw_pass = self.get_argument("password", None)

        # 入力項目の必須チェック
        _errors = []
        if _email == None:
            _errors.append("ID(Email Address) is required.")
        if _raw_pass == None:
            _errors.append("Password is required.")
        if len(_errors) > 0:  # エラーはサインイン画面に渡す
            self.render("signupUser.html", errors=_errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # メールアドレスの重複を許可しない
        if u is not None:
            self.render("signupUser.html", errors=[
                        "The ID(Email Address) cannot be used."], messages=[])
            return

        # ユーザー情報を保存
        u = user()
        u.attr["email"] = _email
        u.attr["password"] = _pass
        u.save()

        # サインイン画面へリダイレクト(サインイン完了の旨を添えて)
        self.redirect("/login?message=%s" % tornado.escape.url_escape(
            "Sign up is complete. Please continue to sign in."))


# サインアップ Artist
class SignupArtistHandler(LoginBaseHandler):
    def get(self):
        # サインイン画面の表示
        self.render("signupArtist.html", errors=[], messages=[])

    def post(self):
        # パラメータの取得
        _email = self.get_argument("email", None)
        _genre = self.get_argument("sound", None)
        _sex = self.get_argument("sex", None)
        _age = self.get_argument("age", None)
        _artist_name = self.get_argument("artist_name", None)
        _raw_pass = self.get_argument("password", None)

        # 入力項目の必須チェック
        errors = []
        if _email == None:
            errors.append("ID(Email Address) is required.")
        if _genre == None:
            errors.append("Genre is required.")
        if _sex == None:
            errors.append("Sex is required.")
        if _age == None:
            errors.append("Age is required.")
        if _artist_name == None:
            errors.append("Artist's name is required.")
        if _raw_pass == None:
            errors.append("Password is required.")
        if len(errors) > 0:  # エラーはサインイン画面に渡す
            self.render("signupArtist.html", errors=errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # メールアドレスの重複を許可しない
        if u is not None:
            self.render("signupArtist.html", errors=[
                        "The ID(Email Address) cannot be used."], messages=[])
            return

        # ユーザー情報を保存
        u = user()
        u.attr["email"] = _email
        u.attr["genre"] = _genre
        u.attr["sex"] = _sex
        u.attr["fan_class"] = _age
        u.attr["artist_name"] = _artist_name
        u.attr["password"] = _pass
        u.save_artist()

        # サインイン画面へリダイレクト(サインイン完了の旨を添えて)
        self.redirect("/loginArtist?message=%s" % tornado.escape.url_escape(
            "Sign up is complete. Please continue to sign in."))
