import ptbot
from decouple import config
from pytimeparse import parse


TG_TOKEN = config('TG_TOKEN')
TG_CHAT_ID = config('TG_CHAT_ID')


def echo(chat_id, message, bot):
    answer = "Время вышло!"
    bot.send_message(chat_id, answer)


def render_progressbar(total,
                       iteration,
                       prefix='',
                       suffix='',
                       length=30,
                       fill='█',
                       zfill='░'
                       ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def reply(chat_id, question, bot):
    seconds = parse(question)
    total = seconds
    message_id = bot.send_message(chat_id, "Запускается")
    bot.create_countdown(seconds,
                         notify,
                         total=total,
                         message_id=message_id,
                         chat_id=chat_id,
                         bot=bot
                         )
    bot.create_timer(seconds,
                     echo,
                     chat_id=chat_id,
                     message=question,
                     bot=bot
                     )


def notify(seconds, message_id, total, bot, chat_id):
    seconds_total = (0 - seconds) + total
    sek = "Осталось секунд:{}".format(seconds)
    remains = (render_progressbar(total, seconds_total))
    text = f"{sek}\n{remains}"
    bot.update_message(chat_id, message_id, text)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
