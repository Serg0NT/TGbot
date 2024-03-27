from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import LEXICON_RU
from game.game_words import users, ATTEMPTS, get_random_word

router = Router()


# Этот хэндлер будет срабатывать на команду "/stat"
@router.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cancel'))
async def process_cancel_comand(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@router.message(F.text.lower().in_(['да', 'ок', 'сыграем', 'игра',
                                    'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_word'] = get_random_word()
        users[message.from_user.id]['user_word'] = '*****'
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал слово из 5 букв, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на слова из 5 букв'
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@router.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, слова из 5 букв'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@router.message(lambda x: x.text and x.text.isalpha() and len(x.text) == 5)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if message.text.lower() == users[message.from_user.id]['secret_word']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали слово!\n\n'
                'Может, сыграем еще?'
            )

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое слово '
                f'было {users[message.from_user.id]["secret_word"]}\n\nДавайте '
                f'сыграем еще?'
            )
        else:
            users[message.from_user.id]['attempts'] -= 1
            ind = -1
            for let in message.text.lower():
                ind += 1
                if let == users[message.from_user.id]["secret_word"][ind]:
                    print(let)
                    users[message.from_user.id]["user_word"][ind] = let.upper()
                elif let in users[message.from_user.id]["secret_word"]:
                    users[message.from_user.id]["user_word"][ind] = let.lower()
            await message.answer(
                f'{users[message.from_user.id]["user_word"]}\n'
                f'У вас осталось {users[message.from_user.id]["attempts"]} попыток')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@router.message()
async def process_other_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, слова из 5 букв'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )
