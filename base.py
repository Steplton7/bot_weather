import psycopg2
from psycopg2 import Error
import config
'''
try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(**config.db)

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    print("Информация о сервере PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    cursor.execute("SELECT version();")
    # Получить результат
    record = cursor.fetchone()
    print("Вы подключены к - ", record, "\n")

    cursor.execute("SELECT * from weather")
    record = cursor.fetchall() #fetchone() 1 ответ
    print("Результат", record)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
'''

class PostresDB:

    def __init__(self, **database):
        self.connection = psycopg2.connect(**database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM weather')
            return self.cursor.fetchone()

    def get_png(self, png):
        with self.connection:
            self.cursor.execute("SELECT * FROM weather WHERE png ='{0}'".format(png))
            return self.cursor.fetchall()

    #def select_weather(self, num):
    #    with self.connection:
    #        return self.cursor.execute('SELECT * FROM music WHERE id = ?', (num,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM weather')
            return len(self.cursor.fetchall())

    def get_user(self, dialog_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM user_bot WHERE dialog_id = '{0}'".format(dialog_id))
            return len(self.cursor.fetchall())

    def set_user(self, dialog_id, user_id, first_name, last_name, status):
        with self.connection:
            self.cursor.execute(f"INSERT INTO user_bot VALUES ('{dialog_id}','{user_id}','{first_name}','{last_name}','{status}')")
            self.connection.commit()

    def close(self):
        self.connection.close()


