from aiogram import Bot


def get_bot(token: str):
    return Bot(token=token)