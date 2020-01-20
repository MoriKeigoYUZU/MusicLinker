import tornado.web
import datetime
from decimal import Decimal
from model.artist import artist
from controller.ArtistMyPageHandler import SigninBaseHandler

class ArtistMyPageHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("")   #ここ飛び先
            return

        #サインインアーティストの取得
        _id = tornado.escape.xhtml(self.current_user)

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None: messages.append(_message)

        # データ取得
        results = artist.find(int(_id))
        self.render("mypageArtist.html", artist=results, messages=messages, errors=[])
        

#TODO
#signinbasehandlerを継承するかどうか(今のとこは仮置き)
#飛び先
#動作確認

