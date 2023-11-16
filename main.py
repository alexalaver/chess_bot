from aiogram import Bot, Dispatcher, types, executor
from data import DataBasa
from aiogram.utils.exceptions import MessageNotModified
import config as cfg
import functions as fnc
import logging
import buttons as bts
import chess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)
db = DataBasa("localhost", "5432", "chess", "chess_user", "chess_pass")

piece_to_emoji = {
    'P': "♙", 'N': "♘", 'B': "♗", 'R': "♖", 'Q': "♕", 'K': "♔",
    'p': "♟", 'n': "♞", 'b': "♝", 'r': "♜", 'q': "♛", 'k': "♚"
}

def create_board_keyboard(board, highlight_moves=None):
    highlight_moves = highlight_moves or set()
    keyboard = types.InlineKeyboardMarkup()
    for rank in reversed(range(8)):
        row = []
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            emoji = piece_to_emoji.get(piece.symbol(), ' ') if piece else ' '
            callback_data = f"square:{chess.square_name(square)}"
            if square in highlight_moves:
                callback_data = f"move:{chess.square_name(square)}"
                emoji = "**"
            row.append(types.InlineKeyboardButton(emoji, callback_data=callback_data))
        keyboard.row(*row)
    return keyboard


def create_promotion_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    pieces = ["q", "r", "b", "n"]
    for piece in pieces:
        button = types.InlineKeyboardButton(piece_to_emoji[piece.upper()], callback_data=f"promote_to:{piece}")
        keyboard.insert(button)
    return keyboard

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('square:'))
async def select_square(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if db.check_game(user_id):
        board = chess.Board(db.select_board(user_id))
        white_player_id, black_player_id = db.select_players(user_id)
        if (board.turn == chess.WHITE and user_id != white_player_id) or \
           (board.turn == chess.BLACK and user_id != black_player_id):
            await callback_query.answer("Сейчас не ваш ход")
            return

        message_id_two = db.check_message_ids(user_id)
        square = chess.square(chess.FILE_NAMES.index(callback_query.data.split(':')[1][0]), int(callback_query.data.split(':')[1][1]) - 1)
        piece = board.piece_at(square)

        # Проверка, соответствует ли выбранная фигура текущему игроку
        if piece is not None and ((board.turn == chess.WHITE and piece.color != chess.WHITE) or (board.turn == chess.BLACK and piece.color != chess.BLACK)):
            await callback_query.answer("Вы играете за " + ("белых" if board.turn == chess.WHITE else "черных"))
            return

        if db.selected_square(user_id) == square:
            db.update_square(user_id, None)
            keyboard = create_board_keyboard(board)
        else:
            db.update_square(user_id, square)
            moves = [move.to_square for move in board.legal_moves if move.from_square == square]
            highlight_moves = set(moves) if moves else None
            keyboard = create_board_keyboard(board, highlight_moves=highlight_moves)

        try:
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id_two, reply_markup=keyboard)
        except MessageNotModified:
            pass

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('move:'))
async def make_move(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if db.check_game(user_id):
        selected_square = db.selected_square(user_id)
        if selected_square is None:
            await callback_query.answer("Ошибка: начальная клетка не выбрана.")
            return
        two_user_id = db.check_two_user_id(user_id)
        fen = db.select_board(user_id)
        board = chess.Board(fen)
        to_square = chess.square(chess.FILE_NAMES.index(callback_query.data.split(':')[1][0]), int(callback_query.data.split(':')[1][1]) - 1)
        message_id_two = db.check_message_ids(user_id)
        message_id = db.select_message_id_chess(user_id)
        move = chess.Move(selected_square, to_square)
        if move in board.legal_moves:
            is_promotion = (board.piece_type_at(move.from_square) == chess.PAWN and
                            (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7))
            if is_promotion:
                promotion_square = move.to_square
                db.update_promotion_square(user_id, promotion_square)
                keyboard = create_promotion_keyboard()
                await bot.send_message(callback_query.from_user.id, "Выберите фигуру для превращения пешки", reply_markup=keyboard)
            else:
                board.push(move)
                fen = board.fen()
                db.update_board(user_id, fen)
                keyboard = create_board_keyboard(board)
                await bot.edit_message_reply_markup(chat_id=two_user_id, message_id=message_id, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id_two, reply_markup=keyboard)
        else:
            await callback_query.answer("Невозможный ход")

        if board.is_checkmate():
            await bot.send_message(callback_query.from_user.id, "МАТ СДЕЛАН")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('promote_to:'))
async def promote_pawn(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if db.check_game(user_id):
        selected_square = db.selected_square(user_id)
        promotion_square = db.select_promotion_square(user_id)
        board = chess.Board(db.select_board(user_id))
        promote_to = callback_query.data.split(':')[1]
        move = chess.Move(selected_square, promotion_square, chess.Piece.from_symbol(promote_to.upper()))

        if move in board.legal_moves:
            board.push(move)
            keyboard = create_board_keyboard(board)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, text="Доска обновлена", reply_markup=keyboard)
        else:
            await callback_query.answer("Невозможный ход")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        if db.check_game(user_id) is None or db.check_queue_user(user_id):
            if(not db.check_user(user_id)):
                db.add_user(user_id, first_name, username)

            markup_reply = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            markup_reply.add(cfg.button_profile, cfg.button_game)
            markup_reply.row(cfg.button_support, cfg.button_settings)
            await message.answer(cfg.begin_text(fnc.nick_with_link("пользователь", user_id)), reply_markup=markup_reply, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.error_command_text_game)

@dp.message_handler()
async def other_text(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.check_game(user_id) is None and db.check_queue_user(user_id) is None:
            if message.text == cfg.button_game:
                markup_inline = types.InlineKeyboardMarkup(row_width=2)
                markup_inline.add(
                    types.InlineKeyboardButton(cfg.button_chess, callback_data="chess_game")
                )
                await message.answer(cfg.game_enter_text(fnc.nick_with_link("пользователь", user_id)), reply_markup=markup_inline, parse_mode=types.ParseMode.MARKDOWN)
        elif db.check_game(user_id):
            if message.text == "/cancel":
                two_user_id = db.check_two_user_id(user_id)
                db.delete_game_chess(user_id)
                await message.answer(cfg.cancel_text)
                await dp.bot.send_message(two_user_id, cfg.cancel_text_two)
        else:
            await message.answer(cfg.error_command_text_game)

@dp.callback_query_handler()
async def other_buttons(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        user_id = callback_query.from_user.id
        if callback_query.data == "chess_game":
            if db.check_queue() is None:
                markup_inline = types.InlineKeyboardMarkup(row_width=1)
                markup_inline.add(
                    types.InlineKeyboardButton(cfg.button_cancel, callback_data="cancel_chess_queue")
                )
                message = await callback_query.message.edit_text(text=cfg.queue_text, reply_markup=markup_inline)
                db.add_queue_chess(user_id, message.message_id)
            elif db.check_queue() is not None:
                two_user_id = db.check_queue()[0]
                two_user_message_id = db.check_queue()[1]
                db.delete_queue_chess()
                board = chess.Board()
                fen = board.fen()
                keyboard = create_board_keyboard(board)
                message_ids = await callback_query.message.edit_text(text=cfg.chess_game_begin, reply_markup=keyboard)
                db.add_game_chess(user_id, two_user_id, two_user_message_id, message_ids.message_id, fen)
                await callback_query.bot.edit_message_text(chat_id=two_user_id, message_id=two_user_message_id, text=cfg.chess_game_begin_two, reply_markup=keyboard)
        elif callback_query.data == "cancel_chess_queue":
            if db.check_queue() is not None:
                db.delete_queue_chess()
                markup_inline = types.InlineKeyboardMarkup(row_width=2)
                markup_inline.add(
                    types.InlineKeyboardButton(cfg.button_chess, callback_data="chess_game")
                )
                await callback_query.answer(cfg.cancel_game_notification, show_alert=True)
                await callback_query.message.edit_text(cfg.game_enter_text(fnc.nick_with_link("пользователь", user_id)), reply_markup=markup_inline, parse_mode=types.ParseMode.MARKDOWN)





if __name__ == "__main__":
    executor.start_polling(dp)