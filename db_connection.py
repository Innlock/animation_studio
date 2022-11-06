import pymysql


def get_db_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="admin",
            database="animation_studio",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
        # finally:
        #     connection.close()

    except Exception as ex:
        print(ex)
