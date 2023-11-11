from aiogram.utils.markdown import link

def nick_with_link(text, user_id):
    return link(f"{text}", f"tg://user?id={user_id}")