import mysql.connector


def get_cursor():
    connection = mysql.connector.connect(user='root',
                                         password='aespa888', host='127.0.0.1', auth_plugin='mysql_native_password', \
                                         database='LingoAmigo', autocommit=True)
    dbconn = connection.cursor()
    return dbconn, connection

def get_dict_cursor():
    
    connection =  mysql.connector.connect(user='root',
                                         password='aespa888', host='127.0.0.1', auth_plugin='mysql_native_password', \
                                         database='LingoAmigo', autocommit=True)
    return connection.cursor(dictionary=True)