from flask import Flask, render_template, request
from translate import translate
from urllib.parse import unquote
from sort import similar, different
app = Flask(__name__)


@app.route("/")
def default():
    return ""


@app.route("/<word>")
def contextly(word):
    nat_lang = request.args.get("nat_lang", "")
    sentence = request.args.get("sentence", "")
    sentence = unquote(sentence)
    translated_word = translate(word, nat_lang)

    similar_sentences = similar(word, sentence)
    diff_sentences = different(word, sentence)

    params = {word: word, translated_word: translated_word, sentence: sentence}

    return render_template("contextly.html", word=word, translated_word=translated_word, sentence=sentence, similar_sentences=similar_sentences, diff_sentences=diff_sentences)
