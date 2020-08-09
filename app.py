from flask import Flask,render_template,request,jsonify,flash
from flask_bootstrap import Bootstrap
import pymysql
import mydb
from gevent import monkey

monkey.patch_all()
app = Flask(__name__)
bootstrap = Bootstrap(app)



@app.route("/")
def Home():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    # 将研报信息上传到网页
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    # 将财经日历的信息上传到网页
    conn.close()
    return render_template("Home.html", u=u)

#进入登录页面
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/dlogin")
def dlogin():
    name = request.args.get("uname")
    pwd = request.args.get("upwd")
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cls = conn.cursor()
    cls.execute("select * from zhuce where uname=%s and upwd=%s", [name, pwd])
    result = cls.fetchone()
    print(result)
    if result is None:
        flash("user or password not true")
        return render_template("login.html")
    else:
        # 获取研报分析
        sql = "select * from yanbaofenxi"
        cls.execute(sql)
        u = cls.fetchall()
        # 获取财经日历的数据
        conn.close()
        return render_template("Home.html", u=u)

@app.route("/duser")
def douser():
    name = request.args.get("uname")
    pwd = request.args.get("upwd")
    print(name, pwd)
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cls = conn.cursor()
    cls.execute("select * from zhuce where uname=%s and upwd=%s", [name, pwd])
    result = cls.fetchone()
    print(result)
    if result is True:
        exit()
    else:
        rows = cls.execute("insert into zhuce(uname,upwd)values(%s,%s)", [name, pwd])
        conn.commit()
        if rows >= 1:
            return render_template("login.html")
        else:
            return render_template("user.html")
@app.route("/checkUName")
def checkUName():
    name = request.args.get("name")
    return mydb.selectName(name)


@app.route("/Order-List")
def Order_List():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    # 将龙虎榜的数据上传至龙虎榜
    sql = "select * from erp_source"
    cur.execute(sql)
    u = cur.fetchall()
    # 将研报分析的数据上传至龙虎榜页面
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    v = cur.fetchall()
    # 将财经日历的数据上传至龙虎榜页面
    conn.close()
    return render_template("Order-List.html", u=u, v=v)


@app.route("/Price-Limit")
def Price_Limit():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from today_zhangdie"
    cur.execute(sql)
    u = cur.fetchall()
    sql = "select * from riqi"
    cur.execute(sql)
    v = cur.fetchall()
    # 将研报分析的数据上传至涨跌停页面
    sql = "select * from yanbaofenxi "
    cur.execute(sql)
    m = cur.fetchall()
    # 将财经日历的数据上传至涨跌停页面
    conn.close()
    return render_template("Price-Limit.html", u=u, v=v, m=m)


@app.route("/Research-Report")
def Research_Report():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    # 将财经日历数据上传至网页
    conn.close()
    return render_template("Research-Report.html", u=u)



@app.route("/Research-Report-2")
def Research_Report_2():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template("Research-Report-2.html", u=u)


@app.route("/Research-Report-3")
def Research_Report_3():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template("Research-Report-3.html", u=u)
@app.route("/Research-Report-4")
def Research_Report_4():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template("Research-Report-4.html", u=u)


@app.route("/Research-Report-5")
def Research_Report_5():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template("Research-Report-5.html", u=u)

@app.route("/Economic-Calendar")
def Economic_Calendar():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()

    return render_template("Economic-Calendar.html",u=u)





@app.route("/Team")
def Team():
    conn = pymysql.connect(host='jys.chinanorth.cloudapp.chinacloudapi.cn', user='root',
                           password='lzh15679642501', db='dragon list', charset='utf8')
    cur = conn.cursor()
    sql = "select * from yanbaofenxi"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template("Team.html",u=u)





if __name__ == '__main__':
    app.run()
