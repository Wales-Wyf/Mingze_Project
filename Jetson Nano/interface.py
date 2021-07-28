import pymysql
import time

def db_insert(cursor, table, time, id ,name, value):
    sql = "INSERT INTO %s(time, id ,name, value) VALUES ('%s', '%s', '%s', '%s')" % (table, time, id, name, value)
    cursor.execute(sql)


def db_update(cursor, table, time, name, value):
    sql = "UPDATE %s SET time='%s', value='%s' WHERE name='%s'" % (table, time, value, name)
    cursor.execute(sql)


def db_read(cursor, table, name, num):               # num 为倒序读取数据条目数，0表示读取全部
    data=0
    if num == 0:
        sql = "SELECT %s, %s, %s, %s FROM %s WHERE name='%s'" % ('time', 'id', 'name', 'value', table, name)
        cursor.execute(sql)
        data = cursor.fetchall()
    else:
        sql = "SELECT %s, %s, %s, %s FROM %s WHERE name='%s' order by time DESC limit %d" % ('time', 'id', 'name', 'value', table, name, num)
        cursor.execute(sql)
        data = cursor.fetchall()
    return data

def write_sensor_occupant(IP = '192.168.4.33', occupant_num = 0, occupant_transform = 0):
    db = pymysql.connect(host=IP, port=3306,user="root", passwd="cfins", db="data",charset='utf8')
    cursor = db.cursor()
   # sql='select * from sensor_occupant sub order by time desc;'
    #cursor.execute(sql)
    #info1 = cursor.fetchall()
    #db.commit()
   # current_time_cost = info1[0][0]
   # time = current_time_cost+1
    db_time=pymysql.escape_string(time.strftime("%Y-%m-%d %H:%M:%S"))
    occupant_num=pymysql.escape_string(str(occupant_num))
    occupant_transform=pymysql.escape_string(str(occupant_transform))
   

    data1 = db_read(cursor, 'sensor_occupant','occupant_num', 0)
    if data1:
        sql="UPDATE sensor_occupant SET time ='%s' ,value ='%s' WHERE id = '0x00000810';"%(db_time,occupant_num)   
        cursor.execute(sql)
    else:
        sql="insert into sensor_occupant (time, id, name, value) VALUES ('%s','%s','%s',%s);"%(db_time,"0x00000810","occupant_num",occupant_num)
        print(sql)
        cursor.execute(sql)
        
    data1 = db_read(cursor, 'sensor_occupant','occupant_transform',0)
    if data1:
        sql="UPDATE sensor_occupant SET time ='%s' ,value ='%s' WHERE id = '0x00000818';"%(db_time,occupant_transform)   
        cursor.execute(sql)
    else:
        sql="insert into sensor_occupant (time, id, name, value) VALUES ('%s','%s','%s',%s);"%(db_time,"0x00000818","occupant_transform",occupant_transform)
        cursor.execute(sql)
    
    sql="insert into sensor_occupant_his (time, id, name, value) VALUES ('%s','%s','%s',%s);"%(db_time,"0x00000810","occupant_num",occupant_num)
    cursor.execute(sql)
    
    sql="insert into sensor_occupant_his (time, id, name, value) VALUES ('%s','%s','%s',%s);"%(db_time,"0x00000818","occupant_transform",occupant_transform)
    cursor.execute(sql)
    db.commit()


