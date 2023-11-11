import psycopg2

class DataBasa:
    def __init__(self, host1, port1, data, user1, password1):
        self.connect = psycopg2.connect(
            host=host1,
            port=port1,
            database=data,
            user=user1,
            password=password1
        )
        self.cursor = self.connect.cursor()

    def add_user(self, id, first_name, username):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, first_name, username) VALUES(%s, %s, %s)", (id, first_name, username,))
            self.connect.commit()

    def check_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT id FROM users WHERE id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def check_game(self, id):
        with self.connect:
            self.cursor.execute(f"SELECT CASE WHEN id_1 = {id} THEN id_1 WHEN id_2 = {id} THEN id_2 END AS selected_id FROM chess_game")
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def check_two_user_id(self, id):
        with self.connect:
            self.cursor.execute(f"SELECT CASE WHEN id_1 = {id} THEN id_2 WHEN id_2 = {id} THEN id_1 END AS selected_id FROM chess_game")
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def check_queue(self):
        with self.connect:
            self.cursor.execute("SELECT id FROM chess_queue")
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def check_queue_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT id FROM chess_queue WHERE id=%s", (id,))
            return self.cursor.fetchone()

    def add_queue_chess(self, id):
        with self.connect:
            self.cursor.execute("INSERT INTO chess_queue(id) VALUES(%s)", (id,))
            self.connect.commit()

    def delete_queue_chess(self):
        with self.connect:
            self.cursor.execute("DELETE FROM chess_queue")
            self.connect.commit()

    def add_game_chess(self, id_1, id_2):
        with self.connect:
            self.cursor.execute("INSERT INTO chess_game(id_1, id_2, queue) VALUES(%s, %s, %s)", (id_1, id_2, id_2,))
            self.connect.commit()

    def delete_game_chess(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            self.connect.commit()