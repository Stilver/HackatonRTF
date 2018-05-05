#! -*- coding: utf-8 -*-

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
        result = Magic().reformat_chains(subs["subscriber"])
        return render_template("do_the_thing.html", channels=result) if result else "Nothing was found!"


if __name__ == "__main__":
    app.run(HOSTNAME, PORT, debug=True)
