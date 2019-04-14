from flask import Flask, render_template, request
from translate import translate
app = Flask(__name__)


@app.route("/")
def default():
    return ""


@app.route("/<word>")
def contextly(word):
    nat_lang = request.args.get("nat_lang", "")
    translated_word = translate(word, nat_lang)
    return render_template("contextly.html", word=word, translated_word=translated_word, nat_lang=nat_lang)
