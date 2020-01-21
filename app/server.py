#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import sys
from model.user import user
from controller.AuthenticationHandlers import LoginBaseHandler, LoginUserHandler, LoginArtistHandler, SignupUserHandler, SignupArtistHandler, SignoutHandler
from controller.SearchHandlers import TopHandler, SearchHandler, SearchResultsHandler
from controller.ArtistHandlers import ArtistMyPageHandler, UserMyPageHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/top")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        # ダッシュボードを表示
        if _signedInUser.attr["artist_name"] == None:
            self.render("mypageUser.html", user=_signedInUser)
        else:
            self.render("mypageArtist.html", user=_signedInUser)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/top", TopHandler),
    (r"/login", LoginUserHandler),
    (r"/loginArtist", LoginArtistHandler)
    (r"/signupUser", SignupUserHandler),
    (r"/signupArtist", SignupArtistHandler),
    (r"/signout", SignoutHandler),

    # mypage　表示
    (r"/mypageUser", UserMyPageHandler),
    (r"/mypageArtist", ArtistMyPageHandler),

    # search
    (r"/search", SearchHandler),
    # searchResults
    (r"/searchResults", SearchResultsHandler),
],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static"),
    # cookieの暗号化キー(システムごとにランダムな文字列を設定する)
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",
)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "migrate":
            user.migrate()
        if args[1] == "db_cleaner":
            user.db_cleaner()
        if args[1] == "help":
            print("usage: python server.py migrate # prepare DB")
            print("usage: python server.py db_cleaner # remove DB")
            print("usage: python server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
