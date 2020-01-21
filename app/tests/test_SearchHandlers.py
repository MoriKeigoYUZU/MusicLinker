# import unittest
# import datetime
# import copy
# from controller import SearchHandlers
# from unittest import mock
# from model.project import project
# from model.user import user


# class TestSearchHandlers(unittest.TestCase):

#     def test_SearchHandler(self):
#         self.assertEqual(SearchHandlers.SearchHandler())


# if __name__ == '__main__':
#     # unittestを実行
#     unittest.main()

# from django import test
# from django.shortcuts import render
# from requests_html import HTML


# class TestThreadList(test.TestCase):
#     def test_render(self):

#         # テンプレートに投入するデータの準備
#         comments = []
#         for num in range(4):
#             comments.append({
#                 'comment_id': num,
#                 'title': 'title'+str(num),
#             })
#         response_param = {
#             'comments': comments,
#         }

#         # レンダリングする
#         rendered = render(None, 'searchResults.html', response_param)

#         # HTMLパーサを準備してパース
#         parser = HTML(html=rendered.content.decode())
#         # aタグのリストを取得
#         elements = parser.find('a')

#         for index in range(len(comments)):
#             element = elements[index]
#             # textアトリビュートかあらaタグの中身を取得して比較する。
#             self.assertEqual(element.text, "title"+str(index))
