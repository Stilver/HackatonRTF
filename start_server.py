#! -*- coding: utf-8 -*-

import sys
import traceback
import logging

from Magic import Magic
from flask import Flask, render_template, request
from settings import *

app = Flask(__name__)


reasons = [
    'Узнать о тарифах',
    'Смена тарифа',
    'Смена сим-карты с сохраниением нормера',
    'Переоформление номера на другое лицо',
    'Красивый номер',
    'Подключенные услуги',
    'Причина списание средств',
    'Остаток интернет трафика',
    'Проблема со связью',
    'Сменить пароль ЛК',
    'Детализация счета',
    'Узнать баланс',
    'Средства не поступили на счет',
    'Подключение/отключение услуги'
]


@app.route("/")
def index():
    return render_template("index.html", reasons=reasons)


@app.route("/do_the_thing", methods=['POST'])
def get_channels():
    subs = request.form
    subs.to_dict()
    try:
        for subs_id in subs["subscriber"].split(","):
            subs_id = int(subs_id) if subs_id else None
    except ValueError:
        logging.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        logging.error("".join(traceback.format_tb(sys.exc_info()[2])))
        return "Incorrect subscriber ID: '{}'! Consider to use another one!".format(subs_id)
    else:
        result = Magic().reformat_chains(subs["subscriber"], subs.get("reason", 0))
        return render_template("do_the_thing.html", channels=result) if result else "Nothing was found!"

# @app.route("/test", methods=['GET'])
# def get_channelses():
#     result = Magic().reformat_chains()
#     result = []
#     return render_template("do_the_thing.html", channels=result) if result else "Nothing was found!"


if __name__ == "__main__":
    app.run(HOSTNAME, PORT, debug=True)
