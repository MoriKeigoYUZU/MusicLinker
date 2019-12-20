import tornado.web
import MySQLdb
import datetime
import json
from decimal import Decimal
from model.project import project
from model.user import user
from db import DBConnector
from controller.AuthenticationHandlers import SigninBaseHandler


class IncomeRankHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    summary
                ,   SUM(income) AS sum_income
                FROM
                    table_cashbook
                WHERE
                    user_id = %s
                AND income != 0
                GROUP BY
                    summary
                ORDER BY
                    sum_income DESC;
            """, (int(_id), ))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        
        
        response = {}
        response["labels"] = []
        response["values"] = []
        for data in results:
            response["labels"].append(data["summary"])
            response["values"].append(str(data["sum_income"]))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(response))
        

class ExpensesRankHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    summary
                ,   SUM(expenses) AS sum_expenses
                FROM
                    table_cashbook
                WHERE
                    user_id = %s
                AND expenses != 0
                GROUP BY
                    summary
                ORDER BY
                    sum_expenses DESC;
            """, (int(_id), ))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        
        
        response = {}
        response["labels"] = []
        response["values"] = []
        for data in results:
            response["labels"].append(data["summary"])
            response["values"].append(str(data["sum_expenses"]))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(response))

class MonthlyReportHandler(SigninBaseHandler):
    def get(self, ym): # ymを引数で取得する
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        yyyy, mm = divmod(int(ym), 100)

        targetYm = datetime.date(yyyy, mm, 1)

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SET @target = %s;", (targetYm,))
            cursor.execute("SET @user_id = %s;", (int(_id),))
            cursor.execute("""
                SELECT
                    D.`DATE` AS label
                ,   IFNULL(SUM(table_cashbook.income),0) AS income
                ,   -1 * IFNULL(SUM(table_cashbook.expenses),0) AS expenses
                ,   IFNULL((
                        SELECT
                            sum(amount)
                        FROM
                            table_cashbook
                        WHERE
                            `date` <= D.`DATE`
                        AND `user_id` = @user_id
                    ),0) AS total_amount
                FROM (
                    SELECT
                        CAST(DATE_FORMAT(DATE_ADD(@target, INTERVAL NUM.seq DAY), '%Y%m') AS SIGNED) AS YM
                    ,   DATE_ADD(@target, INTERVAL NUM.seq DAY) AS `DATE`
                    FROM (
                        SELECT 0 AS seq FROM DUAL WHERE (@num := 0 - 1) * 0
                        UNION ALL
                        SELECT @num := @num + 1 FROM `information_schema`.COLUMNS LIMIT 31
                    ) AS NUM
                    HAVING
                        YM = CAST(DATE_FORMAT(@target, '%Y%m') AS SIGNED)
                ) AS D
                LEFT OUTER JOIN
                    table_cashbook
                    ON  D.`DATE` = table_cashbook.`date`
                    AND table_cashbook.`user_id` = @user_id
                GROUP BY
                    D.`DATE`;
            """)
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        
        
        response = {}
        response["labels"] = []
        response["chartIncome"] = []
        response["chartExpenses"] = []
        response["chartAmount"] = []
        for data in results:
            response["labels"].append(data["label"])
            response["chartIncome"].append(str(data["income"]))
            response["chartExpenses"].append(str(data["expenses"]))
            response["chartAmount"].append(str(data["total_amount"]))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(response))
        
        
        