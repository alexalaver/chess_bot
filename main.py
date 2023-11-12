from aiogram import Bot, Dispatcher, types, executor
from data import DataBasa
import config as cfg
import functions as fnc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)
db = DataBasa("localhost", "5432", "chess", "chess_user", "chess_pass")


async def buttons_chess():
    markup_inline = types.InlineKeyboardMarkup(row_width=8)
    markup_inline.add(
        types.InlineKeyboardButton("♜", callback_data="♜ 1"),
        types.InlineKeyboardButton("♞", callback_data="♞ 2"),
        types.InlineKeyboardButton("♝", callback_data="♝ 3"),
        types.InlineKeyboardButton("♛", callback_data="♛ 4"),
        types.InlineKeyboardButton("♚", callback_data="♚ 5"),
        types.InlineKeyboardButton("♝", callback_data="♝ 6"),
        types.InlineKeyboardButton("♞", callback_data="♞ 7"),
        types.InlineKeyboardButton("♜", callback_data="♜ 8"),
        types.InlineKeyboardButton("♟", callback_data="♟ 9"),
        types.InlineKeyboardButton("♟", callback_data="♟ 10"),
        types.InlineKeyboardButton("♟", callback_data="♟ 11"),
        types.InlineKeyboardButton("♟", callback_data="♟ 12"),
        types.InlineKeyboardButton("♟", callback_data="♟ 13"),
        types.InlineKeyboardButton("♟", callback_data="♟ 14"),
        types.InlineKeyboardButton("♟", callback_data="♟ 15"),
        types.InlineKeyboardButton("♟", callback_data="♟ 16"),
        types.InlineKeyboardButton(" ", callback_data="17"),
        types.InlineKeyboardButton(" ", callback_data="18"),
        types.InlineKeyboardButton(" ", callback_data="19"),
        types.InlineKeyboardButton(" ", callback_data="20"),
        types.InlineKeyboardButton(" ", callback_data="21"),
        types.InlineKeyboardButton(" ", callback_data="22"),
        types.InlineKeyboardButton(" ", callback_data="23"),
        types.InlineKeyboardButton(" ", callback_data="24"),
        types.InlineKeyboardButton(" ", callback_data="25"),
        types.InlineKeyboardButton(" ", callback_data="26"),
        types.InlineKeyboardButton(" ", callback_data="27"),
        types.InlineKeyboardButton(" ", callback_data="28"),
        types.InlineKeyboardButton(" ", callback_data="29"),
        types.InlineKeyboardButton(" ", callback_data="30"),
        types.InlineKeyboardButton(" ", callback_data="31"),
        types.InlineKeyboardButton(" ", callback_data="32"),
        types.InlineKeyboardButton(" ", callback_data="33"),
        types.InlineKeyboardButton(" ", callback_data="34"),
        types.InlineKeyboardButton(" ", callback_data="35"),
        types.InlineKeyboardButton(" ", callback_data="36"),
        types.InlineKeyboardButton(" ", callback_data="37"),
        types.InlineKeyboardButton(" ", callback_data="38"),
        types.InlineKeyboardButton(" ", callback_data="39"),
        types.InlineKeyboardButton(" ", callback_data="40"),
        types.InlineKeyboardButton(" ", callback_data="41"),
        types.InlineKeyboardButton(" ", callback_data="42"),
        types.InlineKeyboardButton(" ", callback_data="43"),
        types.InlineKeyboardButton(" ", callback_data="44"),
        types.InlineKeyboardButton(" ", callback_data="45"),
        types.InlineKeyboardButton(" ", callback_data="46"),
        types.InlineKeyboardButton(" ", callback_data="47"),
        types.InlineKeyboardButton(" ", callback_data="48"),
        types.InlineKeyboardButton("♙", callback_data="♙ 49"),
        types.InlineKeyboardButton("♙", callback_data="♙ 50"),
        types.InlineKeyboardButton("♙", callback_data="♙ 51"),
        types.InlineKeyboardButton("♙", callback_data="♙ 52"),
        types.InlineKeyboardButton("♙", callback_data="♙ 53"),
        types.InlineKeyboardButton("♙", callback_data="♙ 54"),
        types.InlineKeyboardButton("♙", callback_data="♙ 55"),
        types.InlineKeyboardButton("♙", callback_data="♙ 56"),
        types.InlineKeyboardButton("♖", callback_data="♖ 57"),
        types.InlineKeyboardButton("♘", callback_data="♘ 58"),
        types.InlineKeyboardButton("♗", callback_data="♗ 59"),
        types.InlineKeyboardButton("♕", callback_data="♕ 60"),
        types.InlineKeyboardButton("♔", callback_data="♔ 61"),
        types.InlineKeyboardButton("♗", callback_data="♗ 62"),
        types.InlineKeyboardButton("♘", callback_data="♘ 63"),
        types.InlineKeyboardButton("♖", callback_data="♖ 64"),
    )


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
                markup_inline = await buttons_chess()
                two_user_id = db.check_two_user_id(user_id)
                db.delete_game_chess(user_id)
                await message.answer(cfg.cancel_text, reply_markup=markup_inline)
                await dp.bot.send_message(two_user_id, cfg.cancel_text_two, reply_markup=markup_inline)
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
                db.add_queue_chess(user_id)
                await callback_query.message.edit_text(text=cfg.queue_text, reply_markup=markup_inline)
            elif db.check_queue() is not None:
                markup_inline = types.InlineKeyboardMarkup(row_width=8)
                markup_inline.add(
                    types.InlineKeyboardButton("♜", callback_data="♜ 1"),
                    types.InlineKeyboardButton("♞", callback_data="♞ 2"),
                    types.InlineKeyboardButton("♝", callback_data="♝ 3"),
                    types.InlineKeyboardButton("♛", callback_data="♛ 4"),
                    types.InlineKeyboardButton("♚", callback_data="♚ 5"),
                    types.InlineKeyboardButton("♝", callback_data="♝ 6"),
                    types.InlineKeyboardButton("♞", callback_data="♞ 7"),
                    types.InlineKeyboardButton("♜", callback_data="♜ 8"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 9"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 10"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 11"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 12"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 13"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 14"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 15"),
                    types.InlineKeyboardButton("♟", callback_data="♟ 16"),
                    types.InlineKeyboardButton(" ", callback_data="17"),
                    types.InlineKeyboardButton(" ", callback_data="18"),
                    types.InlineKeyboardButton(" ", callback_data="19"),
                    types.InlineKeyboardButton(" ", callback_data="20"),
                    types.InlineKeyboardButton(" ", callback_data="21"),
                    types.InlineKeyboardButton(" ", callback_data="22"),
                    types.InlineKeyboardButton(" ", callback_data="23"),
                    types.InlineKeyboardButton(" ", callback_data="24"),
                    types.InlineKeyboardButton(" ", callback_data="25"),
                    types.InlineKeyboardButton(" ", callback_data="26"),
                    types.InlineKeyboardButton(" ", callback_data="27"),
                    types.InlineKeyboardButton(" ", callback_data="28"),
                    types.InlineKeyboardButton(" ", callback_data="29"),
                    types.InlineKeyboardButton(" ", callback_data="30"),
                    types.InlineKeyboardButton(" ", callback_data="31"),
                    types.InlineKeyboardButton(" ", callback_data="32"),
                    types.InlineKeyboardButton(" ", callback_data="33"),
                    types.InlineKeyboardButton(" ", callback_data="34"),
                    types.InlineKeyboardButton(" ", callback_data="35"),
                    types.InlineKeyboardButton(" ", callback_data="36"),
                    types.InlineKeyboardButton(" ", callback_data="37"),
                    types.InlineKeyboardButton(" ", callback_data="38"),
                    types.InlineKeyboardButton(" ", callback_data="39"),
                    types.InlineKeyboardButton(" ", callback_data="40"),
                    types.InlineKeyboardButton(" ", callback_data="41"),
                    types.InlineKeyboardButton(" ", callback_data="42"),
                    types.InlineKeyboardButton(" ", callback_data="43"),
                    types.InlineKeyboardButton(" ", callback_data="44"),
                    types.InlineKeyboardButton(" ", callback_data="45"),
                    types.InlineKeyboardButton(" ", callback_data="46"),
                    types.InlineKeyboardButton(" ", callback_data="47"),
                    types.InlineKeyboardButton(" ", callback_data="48"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 49"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 50"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 51"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 52"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 53"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 54"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 55"),
                    types.InlineKeyboardButton("♙", callback_data="♙ 56"),
                    types.InlineKeyboardButton("♖", callback_data="♖ 57"),
                    types.InlineKeyboardButton("♘", callback_data="♘ 58"),
                    types.InlineKeyboardButton("♗", callback_data="♗ 59"),
                    types.InlineKeyboardButton("♕", callback_data="♕ 60"),
                    types.InlineKeyboardButton("♔", callback_data="♔ 61"),
                    types.InlineKeyboardButton("♗", callback_data="♗ 62"),
                    types.InlineKeyboardButton("♘", callback_data="♘ 63"),
                    types.InlineKeyboardButton("♖", callback_data="♖ 64"),
                )
                two_user_id = db.check_queue()
                db.delete_queue_chess()
                db.add_game_chess(user_id, two_user_id)
                message = await callback_query.message.edit_text(text=cfg.chess_game_begin, reply_markup=markup_inline)
                await callback_query.message.edit_text(text=cfg.chess_game_begin, reply_markup=markup_inline)
                await callback_query.bot.edit_message_text(chat_id=two_user_id,message_id=message.message_id, text=cfg.chess_game_begin, reply_markup=markup_inline)
        elif callback_query.data == "cancel_chess_queue":
            if db.check_queue():
                db.delete_queue_chess()
                markup_inline = types.InlineKeyboardMarkup(row_width=2)
                markup_inline.add(
                    types.InlineKeyboardButton(cfg.button_chess, callback_data="chess_game")
                )
                await callback_query.answer(cfg.cancel_game_notification, show_alert=True)
                await callback_query.message.edit_text(cfg.game_enter_text(fnc.nick_with_link("пользователь", user_id)), reply_markup=markup_inline, parse_mode=types.ParseMode.MARKDOWN)



if __name__ == "__main__":
    executor.start_polling(dp)