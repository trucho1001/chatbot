import psycopg2


def ketNoi(host, db, user, passw):
    try:
        conn = psycopg2.connect(host=host, database=db, user=user, password=passw)
        return conn
    except:
        print("Lỗi connect")


def get_user(cur, id_nguoitiepnhan):
    if id_nguoitiepnhan is not None:
        sql = "select firstname, lastname from user_ where userid=" + str(id_nguoitiepnhan)
        cur.execute(sql)
        kq = cur.fetchall()
        name = None
        for row in kq:
            name = row[1] + ' ' + row[0]
        return name
    return None