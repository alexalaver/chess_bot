TOKEN = "6711396076:AAHFiLZR2YgFVY_7mE0JoK4eCS4OoSXgli8"
def begin_text(user):
    return f"🎲 Здравствуйте уважаемый {user}, добро пожаловать в игровой бот! 🎴\n\nДля того чтобы посмотреть какие игры доступны на данный момент, нажмите на кнопку 🎮 Игры 🎮 ниже."

button_profile = "👨‍🌾 Профиль 👨‍🌾"
button_game = "🎮 Игры 🎮"
button_support = "Тех. Поддержка"
button_settings = "🎚️ Настройки 🎚️"

button_chess = "♟ Шахматы ♟"

error_command_text_game = "⚠ Вы не можете использовать данную команду во время игры или очереди! ⚠"
button_cancel = "❌ Отменить ❌"

def game_enter_text(user):
    return f"🎏 Уважаемый {user}, вы можете выбрать игру, в которую хотите поиграть.\nДля этого нажмите на кнопку, один из игр ниже 👇"

queue_text = "⌛ Вы добавлены в очередь, пожалуйста ожидайте ⌛"
cancel_game_notification = "Вы успешно отменили очередь ✅"

chess_game_begin = "🎮 Игра в шахматы ⚠ началась. Вы играете за белых ⚪\n\nЕсли вы хотите прекратить игру, напишите команду /cancel ❌ "
chess_game_begin_two = "🎮 Игра в шахматы ⚠ началась. Вы играете за чёрных ⚫\n\nЕсли вы хотите прекратить игру, напишите команду /cancel ❌"
cancel_text = "Вы успешно прекратили игру ✅"
cancel_text_two = "Ваш соперник прекратил с вами игру ❌"

chess_white_figure = ["♙", "♘", "♗", "♖", "♕", "♔"]
chess_black_figure = ["♟", "♞", "♝", "♜", "♛", "♚"]

error_figure_text_white = "Вы играете за белых!"
error_figure_text_black = "Вы играете за чёрных!"

not_in_game = "Вы не находитесь в игре!"

error_queue_in_game = "Сейчас не ваша очередь!"









# CREATE TABLE chess_game(
# 	id_1 BIGINT,
# 	id_2 BIGINT,
# 	a1 VARCHAR(10) DEFAULT '♜',
# 	a2 VARCHAR(10) DEFAULT '♟',
# 	a3 VARCHAR(10),
# 	a4 VARCHAR(10),
# 	a5 VARCHAR(10),
# 	a6 VARCHAR(10),
# 	a7 VARCHAR(10) DEFAULT '♗',
# 	a8 VARCHAR(10) DEFAULT '♖',
# 	b1 VARCHAR(10) DEFAULT '♞',
# 	b2 VARCHAR(10) DEFAULT '♟',
# 	b3 VARCHAR(10),
# 	b4 VARCHAR(10),
# 	b5 VARCHAR(10),
# 	b6 VARCHAR(10),
# 	b7 VARCHAR(10) DEFAULT '♙',
# 	b8 VARCHAR(10) DEFAULT '♘',
# 	c1 VARCHAR(10) DEFAULT '♝',
# 	c2 VARCHAR(10) DEFAULT '♟',
# 	c3 VARCHAR(10),
# 	c4 VARCHAR(10),
# 	c5 VARCHAR(10),
# 	c6 VARCHAR(10),
# 	c7 VARCHAR(10) DEFAULT '♙',
# 	c8 VARCHAR(10) DEFAULT '♗',
# 	d1 VARCHAR(10) DEFAULT '♛',
# 	d2 VARCHAR(10) DEFAULT '♟',
# 	d3 VARCHAR(10),
# 	d4 VARCHAR(10),
# 	d5 VARCHAR(10),
# 	d6 VARCHAR(10),
# 	d7 VARCHAR(10) DEFAULT '♙',
# 	d8 VARCHAR(10) DEFAULT '♕',
# 	e1 VARCHAR(10) DEFAULT '♚',
# 	e2 VARCHAR(10) DEFAULT '♟',
# 	e3 VARCHAR(10),
# 	e4 VARCHAR(10),
# 	e5 VARCHAR(10),
# 	e6 VARCHAR(10),
# 	e7 VARCHAR(10) DEFAULT '♙',
# 	e8 VARCHAR(10) DEFAULT '♔',
# 	f1 VARCHAR(10) DEFAULT '♝',
# 	f2 VARCHAR(10) DEFAULT '♟',
# 	f3 VARCHAR(10),
# 	f4 VARCHAR(10),
# 	f5 VARCHAR(10),
# 	f6 VARCHAR(10),
# 	f7 VARCHAR(10) DEFAULT '♙',
# 	f8 VARCHAR(10) DEFAULT '♗',
# 	g1 VARCHAR(10) DEFAULT '♞',
# 	g2 VARCHAR(10) DEFAULT '♟',
# 	g3 VARCHAR(10),
# 	g4 VARCHAR(10),
# 	g5 VARCHAR(10),
# 	g6 VARCHAR(10),
# 	g7 VARCHAR(10) DEFAULT '♗',
# 	g8 VARCHAR(10) DEFAULT '♘',
# 	h1 VARCHAR(10) DEFAULT '♜',
# 	h2 VARCHAR(10) DEFAULT '♟',
# 	h3 VARCHAR(10),
# 	h4 VARCHAR(10),
# 	h5 VARCHAR(10),
# 	h6 VARCHAR(10),
# 	h7 VARCHAR(10) DEFAULT '♙',
# 	h8 VARCHAR(10) DEFAULT '♖'
# );