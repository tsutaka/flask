import MySQLdb # pip install mysqlclient
import configparser 
import json
import random

table_dakuon = {
    "カ":"ガ", 
    "キ":"ギ", 
    "ク":"グ", 
    "ケ":"ゲ", 
    "コ":"ゴ", 
    "サ":"ザ", 
    "シ":"ジ", 
    "ス":"ズ", 
    "セ":"ゼ", 
    "ソ":"ゾ", 
    "タ":"ダ", 
    "チ":"ヂ", 
    "ツ":"ヅ", 
    "テ":"デ", 
    "ト":"ド", 
    "ハ":"バ", 
    "ヒ":"ビ", 
    "フ":"ブ", 
    "ヘ":"ベ", 
    "ホ":"ボ"
}

table_handakuon = { 
    "ハ":"パ", 
    "ヒ":"ピ", 
    "フ":"プ", 
    "ヘ":"ペ", 
    "ホ":"ポ"
}
table_seion = {
    "ガ":"カ", 
    "ギ":"キ", 
    "グ":"ク", 
    "ゲ":"ケ", 
    "ゴ":"コ", 
    "ザ":"サ", 
    "ジ":"シ", 
    "ズ":"ス", 
    "ゼ":"セ", 
    "ゾ":"ソ", 
    "ダ":"タ", 
    "ヂ":"チ", 
    "ヅ":"ツ", 
    "デ":"テ", 
    "ド":"ト", 
    "バ":"ハ", 
    "ビ":"ヒ", 
    "ブ":"フ", 
    "ベ":"ヘ", 
    "ボ":"ホ", 
    "パ":"ハ", 
    "ピ":"ヒ", 
    "プ":"フ", 
    "ペ":"ヘ", 
    "ポ":"ホ", 
    "ァ":"ア", 
    "ィ":"イ", 
    "ゥ":"ウ", 
    "ェ":"エ", 
    "ォ":"オ", 
    "ッ":"ツ", 
    "ャ":"ヤ", 
    "ュ":"ユ", 
    "ョ":"ヨ"
}

def open_conn():
    config_ini = configparser.ConfigParser()
    with open('./Chat/config.ini') as fin: # Related path from execute file
        config_ini.read_file(fin, 'UTF-8')
    conn = MySQLdb.connect(
        host=config_ini['DB']['host'],
        port=int(config_ini['DB']['port']),
        db=config_ini['DB']['database'],
        user=config_ini['DB']['user'],
        passwd=config_ini['DB']['password'], 
        charset='utf8'
        )
    
    return conn

def get_enemy_path(conn, name_list):
    path_list = []

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    for name in name_list:
        sql = "SELECT img_path FROM `enemy` WHERE enemy_name='" + name + "'"
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) == 1:
            path_list.append(rows[0]["img_path"])
        else :
            path_list.append("")


    return path_list

def get_current_data(conn):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `shiritori` WHERE status='current'"
    cur.execute(sql)
    rows = cur.fetchall()
    crnt_num = rows[0]["num"]
    crnt_name_list = []
    for name in json.loads(rows[0]["list"]):
        crnt_name_list.append(name)
    crnt_image_list = get_enemy_path(conn, crnt_name_list)
    crnt_last_char = rows[0]["last_char"]

    return crnt_num, crnt_name_list, crnt_image_list, crnt_last_char

def get_candidate_data(conn, name_list, last_char):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT enemy_name FROM `enemy` WHERE enemy_name LIKE '" + last_char + "%' "
    if last_char in table_dakuon:
        sql += "OR enemy_name LIKE '" + table_dakuon[last_char] + "%' "
    
    if last_char in table_handakuon:
        sql += "OR enemy_name LIKE '" + table_dakuon[last_char] + "%' "

    cur.execute(sql)
    rows = cur.fetchall()
    cddt_name_list = []
    for row in rows:
        if row["enemy_name"] not in name_list:
            cddt_name_list.append(row["enemy_name"])

    cddt_num = len(cddt_name_list)
    cddt_image_list = get_enemy_path(conn, cddt_name_list)

    return cddt_num, cddt_name_list, cddt_image_list

def get_hiscore_data(conn):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `shiritori` WHERE status='hiscore'"
    cur.execute(sql)
    rows = cur.fetchall()
    hscore_num = rows[0]["num"]
    hscore_name_list = []
    for name in json.loads(rows[0]["list"]):
        hscore_name_list.append(name)
    hscore_image_list = get_enemy_path(conn, hscore_name_list)

    return hscore_num, hscore_name_list, hscore_image_list

def get_random_data(conn):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `enemy` WHERE img_path <> '' "
    cur.execute(sql)
    rows = cur.fetchall()
    name = rows[random.randint(0, len(rows)-1)]["enemy_name"]

    return name

def get_last_char(name):
    if name[-1:] == "ー":
        name = name[:-1]
    last_char = name[-1:]
    if last_char in table_seion:
        last_char = table_seion[last_char]

    return last_char

def set_init_db(conn, enemy_name, last_char):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "UPDATE `shiritori` SET `num`=1,`list`='"
    sql += '["' + enemy_name + '"]'
    sql += "',`last_char`='" + last_char + "' WHERE status='current' "

    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()

    return

def update_current_db(conn, num, crnt_name_list, name, last_char):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "UPDATE `shiritori` SET `num`=" + str(num) + ",`list`='"
    sql += '['
    for crnt_name in crnt_name_list:
        sql += '"' + crnt_name + '", '
    sql += '"' + name + '"]'
    sql += "',`last_char`='" + last_char + "' WHERE status='current' "

    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()

    return

def update_hiscore_db(conn, num, crnt_name_list, name, last_char):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "UPDATE `shiritori` SET `num`=" + str(num) + ",`list`='"
    sql += '['
    for crnt_name in crnt_name_list:
        sql += '"' + crnt_name + '", '
    sql += '"' + name + '"]'
    sql += "',`last_char`='" + last_char + "' WHERE status='hiscore' "

    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()

    return

def get_data():
    conn = open_conn()
    
    crnt_num, crnt_name_list, crnt_image_list, crnt_last_char = get_current_data(conn)

    cddt_num, cddt_name_list, cddt_image_list = get_candidate_data(conn, crnt_name_list, crnt_last_char)

    hscore_num, hscore_name_list, hscore_image_list = get_hiscore_data(conn)

    conn.close()

    ansjson = {
        "current": {
            "num": crnt_num, 
            "image_list": crnt_image_list, 
            "name_list": crnt_name_list, 
            "last_char": crnt_last_char
        },
        "candidate": {
            "num": cddt_num,  
            "image_list": cddt_image_list, 
            "name_list": cddt_name_list
        },
        "highscore": {
            "num": hscore_num, 
            "image_list": hscore_image_list, 
            "name_list": hscore_name_list
        }
    }
    return ansjson
    
def post_data(name):
    conn = open_conn()
    conn.autocommit(False)

    try:
        crnt_num, crnt_name_list, _, crnt_last_char = get_current_data(conn)

        _, cddt_name_list, _ = get_candidate_data(conn, crnt_name_list, crnt_last_char)
        
        hscore_num, _, _ = get_hiscore_data(conn)

        if name not in cddt_name_list:
            ansjson = { "starus": "failed" }
            conn.rollback()
            return ansjson 
        
        last_char = get_last_char(name)

        update_current_db(conn, crnt_num + 1, crnt_name_list, name, last_char)

        if crnt_num + 1 > hscore_num:
            update_hiscore_db(conn, crnt_num + 1, crnt_name_list, name, last_char)

    except Exception as e:
        conn.rollback()
        print("post error!")
        raise e

    finally:
        conn.close()
    
    ansjson = { "starus": "success" }
    return ansjson 

def post_reset():
    conn = open_conn()
    conn.autocommit(False)
    
    try:
        enemy_name = get_random_data(conn)

        last_char = get_last_char(enemy_name)

        set_init_db(conn, enemy_name, last_char)
    
    except Exception as e:
        conn.rollback()
        print("reset error!")
        raise e

    finally:
        conn.close()
    
    ansjson = {
        "starus": "success"
    }
    return ansjson 