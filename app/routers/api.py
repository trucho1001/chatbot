import json

from fastapi import APIRouter
from pydantic import BaseModel
from pyvi import ViUtils
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.routers.utils.postgreSQL import ketNoi, get_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
router.mount("/static", StaticFiles(directory="app/static"), name="static")

host = 'localhost'
db = 'nckh_chatbot'
user = 'postgres'
passw = '123456'


class FormGetTT(BaseModel):
    id_dv: str
    id_lv: str
    tu_khoa: str


class FormGetHS(BaseModel):
    ten_DN: str
    thoi_gian: str


class FormTimTT(BaseModel):
    id_tt: str


@router.post("/lay_thu_tuc")
async def lay_tt(data: FormGetTT):
    conn = ketNoi(host, db, user, passw)
    cur = conn.cursor()
    if data.id_dv == '0' and data.id_lv == '0':
        sql = "select tt_id,tt_ten from cgate_dm_tthc"
    elif data.id_lv == '0':
        sql = "select tt_id,tt_ten from cgate_dm_tthc where dv_id={}".format(data.id_dv)
    else:
        sql = "select tt_id,tt_ten from cgate_dm_tthc where lv_id={}".format(data.id_lv)

    cur.execute(sql)
    kq = cur.fetchall()
    dict = {}
    KTDB = "„©,.\\/<>?';:'\"[]{}=+-_)(*&^%$#@!~`|“"
    if data.tu_khoa == 'a':
        for row in kq:
            dict.update({row[0]: row[1]})
    else:
        for row in kq:
            ten_tt = row[1]
            ten_tt = ten_tt + ' '
            ten_tt = ten_tt.lower()
            for i in KTDB:
                if ten_tt.find(i) >= 0:
                    ten_tt = ten_tt.replace(i, '')

            # ten_tt = str(ViUtils.remove_accents(ten_tt))[1:]

            if ten_tt.find(data.tu_khoa.lower()) >= 0 and \
                    (ten_tt[ten_tt.find(data.tu_khoa.lower()) + len(data.tu_khoa)] == ' '):
                # print(ten_tt)
                dict.update({row[0]: row[1]})

    conn.close()
    return dict


@router.post("/thutuc")
async def tim_thu_tuc(data: FormTimTT):
    print(data.id_tt)
    conn = ketNoi(host, db, user, passw)
    cur = conn.cursor()
    sql = "select tt_ma,tt_ten,tt_thoihan_gq,ctth_ten,dv_id from cgate_dm_tthc where tt_id={}".format(data.id_tt)
    cur.execute(sql)
    kq = cur.fetchall()
    dic = {}
    for row in kq:
        dic.update({row[0]: {'Thủ tục tên': row[1], 'Thời gian giải quyết': row[2], 'Cách thức thực hiện': row[3],
                             'dv_id': row[4]}})
    conn.close()
    return dic


@router.post("/hoso")
async def tim_ho_so(data: FormGetHS):
    conn = ketNoi(host, db, user, passw)
    cur = conn.cursor()
    sql = "select tccn_id, tccn_ten, tccn_diachi, tccn_phone, ttcn_socmnd_or_dkkd " \
          "from cchc_dm_tochuc_canhan where Lower (tccn_ten)='{}'".format(data.ten_DN.lower())
    cur.execute(sql)
    kq = cur.fetchall()
    dic_tccn = {}
    for row in kq:
        dic_tccn.update({row[0]: {
            'tccn_ten': row[1],
            'tccn_diachi': row[2],
            'tccn_phone': row[3],
            'ttcn_socmnd_or_dkkd': row[4]
        }})
    id_cn = list(dic_tccn.keys())
    date = data.thoi_gian
    dic_kq = {}
    tmp = 0
    for i in id_cn:
        sql1 = "select hs_id, hs_noidung, hs_ngaytiepnhan, hs_ngayhentra, hs_ngaytrakq, userid_tiepnhan," \
               "userid_trakq, tccn_id, hs_ngaytao, hs_ma, hs_ngayxulyxong" \
               " from cchc_ds_hoso where tccn_id={} and hs_ngaytao='{}'".format(i, date)
        cur.execute(sql1)
        kq = cur.fetchall()
        for row in kq:
            if row[10] is not None:
                tinh_trang = 'Đã xử lý xong!'
            else:
                tinh_trang = 'Phong ban chuyên môn đang xử lý!'
            dia_chi = dic_tccn[i]['tccn_diachi']
            tccn_ten = dic_tccn[i]['tccn_ten']
            ten_nguoitiepnhan = get_user(cur, row[5])
            dic_kq.update({tmp: {
                'hsID': row[0],
                'noidung': row[1],
                'ngaytiepnhan': row[2],
                'ngayhentra': row[3],
                'ngaytrakq': row[4],
                'ngayxulyxong': row[10],
                'tinhtranghs': tinh_trang,
                'nguoitiepnhan': ten_nguoitiepnhan,
                'tccn_id': row[7],
                'tccn_ten': tccn_ten,
                'diachi_tccn': dia_chi,
                'hs_ngaytao': row[8],
                'hs_ma': row[9]
            }})
            tmp += 1
    conn.close()
    return dic_kq
