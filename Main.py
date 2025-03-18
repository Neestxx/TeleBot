import telebot
import sqlite3
import random


bot = telebot.TeleBot('7735884605:AAEMGfcUNSZs7cB2CaHhPPuY2XWXUNXN9cE')

guides_ege = {1: 'https://www.youtube.com/watch?v=p6w_gZZl69g',
              2: 'https://www.youtube.com/watch?v=lHMng4c3qw0',
              3: 'https://www.youtube.com/watch?v=ZRB420NAzWs',
              4: 'https://www.youtube.com/watch?v=nKJAH6dcKcs',
              5: 'https://www.youtube.com/watch?v=JgQd7ZkOBiU',
              6: 'https://www.youtube.com/watch?v=esE97ZVqnZ4',
              7: 'https://www.youtube.com/watch?v=Rg_6kDKZ3Yw',
              8: 'https://www.youtube.com/watch?v=NUVNnOMEtBc',
              9: 'https://www.youtube.com/watch?v=1WKJALnNY4o',
              10: 'https://www.youtube.com/watch?v=mSe5ftJvt54',
              11: 'https://www.youtube.com/watch?v=k14Wgtrq7Hc',
              12: 'https://www.youtube.com/watch?v=r875YTbho4E',
              13: 'https://www.youtube.com/watch?v=d24VUoQyDCE',
              14: 'https://www.youtube.com/watch?v=Y6Ep-wkg_yo',
              15: 'https://www.youtube.com/watch?v=g_kAnbPFZw0',
              16: 'https://www.youtube.com/watch?v=IBGGomXu_p8',
              17: 'https://www.youtube.com/watch?v=pWHVMHU6o94',
              18: 'https://www.youtube.com/watch?v=bwpXYik-Tg8',
              19: 'https://www.youtube.com/watch?v=bwpXYik-Tg8',
              20: 'https://www.youtube.com/watch?v=bwpXYik-Tg8',
              21: 'https://www.youtube.com/watch?v=bwpXYik-Tg8',
              22: 'https://www.youtube.com/watch?v=iORWhe7u4nw',
              23: 'https://www.youtube.com/watch?v=7HRlpWKuzYU',
              24: 'https://www.youtube.com/watch?v=wPitnvhU7nU',
              25: 'https://www.youtube.com/watch?v=EZkbcmVmoHA',
              26: 'https://www.youtube.com/watch?v=0p3QjF3ecJA',
              27: 'https://www.youtube.com/watch?v=nBl93kz5miM'
              }

result = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''Привет, я помогу тебе подготовиться к ЕГЭ по информатике. В данном боте ты можешь изучить теорию, по выбранному тобой заданию Ниже я приложу небольшую инструкцию, как мной пользоваться:\n\n /start - Приветственное сообщение, описание бота.\n
/help - помощь в пользовании ботом/связь с создателем бота.\n\n Также Вы можете ввести цифру любого задания из ЕГЭ (из диапазона от 1 до 27) и бот вам выдаст ссылку, по которой Вы можете посмотреть небольшую теорию про выбранное Вами задание.''')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Данный бот предназначен для для учеников, сдающих ЕГЭ. Вы можете изучить теорию по различным номерам ЕГЭ по информатике.\nЕсли у Вас остались какие-либо вопросы, Вы можете написать мне в личные сообщения в Telegram: @Neestxx')




@bot.message_handler(commands=['guides'])
def guide(message):
    bot.send_message(message.chat.id, 'Напишите ниже номер задания ЕГЭ по информатике для помощи по данному заданию.')
    bot.register_next_step_handler(message, index)

def index(message):
    try:
        a = guides_ege[int(message.text)]
        bot.reply_to(message, a)
    except KeyError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите номер задания (от 1 до 27).')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите число.')



@bot.message_handler(commands=['practise'])
def practise_start(message):
    bot.send_message(message.chat.id, 'Здесь ты можешь попрактиковаться в любом задании из ЕГЭ. Введи ниже номер задания, чтобы начать практику.')
    con = sqlite3.connect('data.sqlite3', check_same_thread=False)
    cur = con.cursor()
    tasks = cur.execute('SELECT DISTINCT number FROM data').fetchall()
    res = []
    for i in tasks:
        res.append(str(*i))

    bot.send_message(message.chat.id, f'На данный момент доступны задания: {", ".join(sorted(res, key=lambda x: int(x)))}')
    bot.register_next_step_handler(message, number_practise)

def number_practise(message):
    global result
    try:
        if int(message.text.strip()) not in range(1, 28):
            raise KeyError

        con = sqlite3.connect('data.sqlite3', check_same_thread=False)
        cur = con.cursor()
        selection = cur.execute(f'SELECT task, answer FROM data WHERE number={int(message.text)}').fetchall()
        result = random.choice(selection)

        bot.send_message(message.chat.id, f'Вы выбрали задание {message.text}, вот задание по данному номеру:')
        bot.send_message(message.chat.id, f'{result[0]}')
        bot.register_next_step_handler(message, ans)

    except KeyError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите число из допустимого диапазона')

    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите число')

    except IndexError:
        bot.send_message(message.chat.id, 'К сожалению пока что задание по данному номеру не доступно')


def ans(message):
    right_text = ['Отличный ответ!', 'Правильный ответ, молодец!', 'Молодец, так держать!', 'Поздравляю, верный ответ!']
    try:
        global result
        if message.text.strip() == result[1]:
            bot.reply_to(message, f'{random.choice(right_text)}\nЧтобы начать заново, введите /practise в чат')
        else:
            bot.reply_to(message, f'Неверно, правильный ответ: {result[1]}\nЧтобы попробовать снова, введите команду /practise')
    except KeyError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите допустимое значение')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста, введите число. Чтобы начать заново введите команду /practise')


def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()

