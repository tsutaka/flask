import MySQLdb # pip install mysqlclient
import configparser 

def get_num():
    config_ini = configparser.ConfigParser()
    with open('./chat/config.ini') as fin:　# Related path from execute file
        config_ini.read_file(fin, 'UTF-8')
    conn = MySQLdb.connect(
        host=config_ini['DB']['host'],
        port=int(config_ini['DB']['port']),
        db=config_ini['DB']['database'],
        user=config_ini['DB']['user'],
        passwd=config_ini['DB']['password']
        )
    
    cur = conn.cursor()
    sql = 'SELECT DISTINCT name, ip ' \
        'FROM `chat_user` ' \
        'WHERE DATE_ADD(datetime, INTERVAL 3 MINUTE) > NOW()'
    cur.execute(sql)
    rows = cur.fetchall()
    num = 0
    for row in rows:
        if row[0] != "??????":
            num = num + 1

    conn.close
    ansjson = {
        "num": num
    }
    return ansjson