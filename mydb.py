import  pymysql
def selectName(uname):
    conn = pymysql.connect(
        host="jys.chinanorth.cloudapp.chinacloudapi.cn",
        port=3306,
        user="root",
        password="lzh15679642501",
        db="dragon list",
        charset="utf8"
    )
    print(conn)
    cls = conn.cursor()
    # 前端传递的数据，进行到数据库中进行验证
    cls.execute("select * from zhuce where uname=%s ", [uname])
    result = cls.fetchone()
    if result is None:
        return "false"
    else:
       return "true"
