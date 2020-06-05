import MySQLdb # pip install mysqlclient
import configparser 
import json

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

def get_data():
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
    
    crnt_num, crnt_name_list, crnt_image_list, crnt_last_char = get_current_data(conn)

    cddt_num, cddt_name_list, cddt_image_list = get_candidate_data(conn, crnt_name_list, crnt_last_char)

    hscore_num, hscore_name_list, hscore_image_list = get_hiscore_data(conn)

    conn.close

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