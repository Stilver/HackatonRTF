#! -*- coding: utf-8 -*-

import sys
import traceback
import logging

from Magic import Magic
from flask import Flask, render_template, request
from settings import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", hostname=HOSTNAME, port=PORT)


@app.route("/do_the_thing", methods=['POST', 'GET'])
def get_channels():
    if request.method == 'POST':
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
            result = Magic().reformat_chains(subs["subscriber"])
            return render_template("do_the_thing.html", channels=result) if result else "Nothing was found!"


if __name__ == "__main__":
    app.run(HOSTNAME, PORT, debug=True)
