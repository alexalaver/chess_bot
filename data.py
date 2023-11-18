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

    def check_message_ids(self, id):
        with self.connect:
            self.cursor.execute("SELECT id_1 FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            user_id = self.cursor.fetchone()[0]
            if user_id == id:
                self.cursor.execute("SELECT message_id_two FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
                return self.cursor.fetchone()[0]
            else:
                self.cursor.execute("SELECT message_id FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
                return self.cursor.fetchone()[0]


    def check_figure_white_id(self, id):
        with self.connect:
            self.cursor.execute("SELECT id_1 FROM chess_game WHERE id_1=%s", (id,))
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def check_figure_black_id(self, id):
        with self.connect:
            self.cursor.execute("SELECT id_2 FROM chess_game WHERE id_2=%s", (id,))
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def check_queue(self):
        with self.connect:
            self.cursor.execute("SELECT id, message_id FROM chess_queue")
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a

    def check_queue_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT id FROM chess_queue WHERE id=%s", (id,))
            return self.cursor.fetchone()

    def add_queue_chess(self, id, message_id):
        with self.connect:
            self.cursor.execute("INSERT INTO chess_queue(id, message_id) VALUES(%s, %s)", (id, message_id,))
            self.connect.commit()

    def delete_queue_chess(self):
        with self.connect:
            self.cursor.execute("DELETE FROM chess_queue")
            self.connect.commit()

    def add_game_chess(self, id_1, id_2, message_id, message_id_two, board):
        with self.connect:
            self.cursor.execute("INSERT INTO chess_game(id_1, id_2, message_id, message_id_two, board) VALUES(%s, %s, %s, %s, %s)", (id_1, id_2, message_id, message_id_two, board,))
            self.connect.commit()

    def select_message_id_chess(self, id):
        with self.connect:
            self.cursor.execute("SELECT id_1 FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            user_id = self.cursor.fetchone()[0]
            if user_id == id:
                self.cursor.execute("SELECT message_id FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
                return self.cursor.fetchone()[0]
            else:
                self.cursor.execute("SELECT message_id_two FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
                return self.cursor.fetchone()[0]

    def delete_game_chess(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            self.connect.commit()

    def select_queue_in_game(self, id):
        with self.connect:
            self.cursor.execute("SELECT queue FROM chess_game WHERE queue=%s", (id,))
            a = self.cursor.fetchone()
            if a is None:
                return None
            else:
                return a[0]

    def add_use_chess(self, use_chess):
        with self.connect:
            self.cursor.execute("UPDATE chess_game SET use_chess=%s", (use_chess,))
            self.connect.commit()

    def update_move_chess_pawn_one(self, id, column1):
        with self.connect:
            self.cursor.execute(f"UPDATE chess_game SET {column1}=%s WHERE id_1=%s OR id_2=%s", ("🔸", "🔸", "🔸", id, id,))
            self.connect.commit()

    def update_move_chess_pawn_two(self, id, column1, column2):
        with self.connect:
            self.cursor.execute(f"UPDATE chess_game SET {column1}=%s, {column2}=%s WHERE id_1=%s OR id_2=%s", ("🔸", "🔸", "🔸", id, id,))
            self.connect.commit()

    def update_move_chess_pawn_three(self, id, column1, column2, column3):
        with self.connect:
            self.cursor.execute(f"UPDATE chess_game SET {column1}=%s, {column2}=%s, {column3}=%s WHERE id_1=%s OR id_2=%s", ("🔸", "🔸", "🔸", id, id,))
            self.connect.commit()

    def select_all_board_chess(self, column, id):
        with self.connect:
            self.cursor.execute(f"SELECT {column} FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            a = self.cursor.fetchone()[0]
            if a is None:
                return " "
            else:
                return a

    def select_all_board_chess_hod(self, column, id):
        with self.connect:
            self.cursor.execute(f"SELECT {column} FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            a = self.cursor.fetchone()[0]
            if a is None:
                return None
            else:
                return a


    def select_use_chess(self):
        with self.connect:
            self.cursor.execute("")

    def selected_square(self, id):
        with self.connect:
            self.cursor.execute("SELECT selected_square FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            result = self.cursor.fetchone()
            if result and result[0] is not None:
                try:
                    return int(result[0])
                except ValueError:
                    return None
            else:
                return None

    def select_players(self, id):
        with self.connect:
            self.cursor.execute("SELECT id_1, id_2 FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            return self.cursor.fetchone()

    def update_square(self, id, square):
        with self.connect:
            self.cursor.execute("UPDATE chess_game SET selected_square=%s WHERE id_1=%s OR id_2=%s", (square, id, id,))
            self.connect.commit()

    def update_board(self, id, board):
        with self.connect:
            self.cursor.execute("UPDATE chess_game SET board=%s WHERE id_1=%s OR id_2=%s", (board, id, id,))
            self.connect.commit()

    def select_board(self, id):
        with self.connect:
            self.cursor.execute("SELECT board FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            return self.cursor.fetchone()[0]

    def select_promotion_square(self, id):
        with self.connect:
            self.cursor.execute("SELECT promotion_square FROM chess_game WHERE id_1=%s OR id_2=%s", (id, id,))
            return self.cursor.fetchone()[0]

    def update_promotion_square(self, id, promotion):
        with self.connect:
            self.cursor.execute("UPDATE chess_game SET promotion_square=%s WHERE id_1=%s OR id_2=%s", (promotion, id, id,))
            self.connect.commit()

    def update_current_turn(self, id, current):
        with self.connect:
            self.cursor.execute("UPDATE chess_game SET current_turn=%s WHERE id_1=%s OR id_2=%s", (current, id, id,))
            self.connect.commit()