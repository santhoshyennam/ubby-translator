from flask import Flask, redirect, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    file = open("translated.csv","r")
    reader = csv.reader(file)
    sentences = list(reader)
    file.close()
    print("len",len(sentences))
    return render_template("index.html",sentences = sentences)

@app.route('/translate', methods= ["GET","POST"])
def translate():
    if request.method == "GET":
        return render_template("translate.html")
    elif request.method == "POST":
        if not request.form.get("text").strip():
            return render_template("failure.html",error="text should not be empty")
        file = open("translated.csv","a")
        writer = csv.writer(file)
        text =ubby_translator(request.form.get("text").strip())
        writer.writerow([text])
        file.close()
        return redirect("/")

@app.route("/reverse")
def reverse():
    file = open("translated.csv","r")
    reader = csv.reader(file)
    sentences = list(reader)
    file.close()
    untranslated_sentences = []
    for sentence in sentences:
        untranslated_sentences.append(unubby_translator(sentence[0]))
    return render_template("reverse.html",sentences = untranslated_sentences)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

def ubby_translator(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    ubby_text = ''
    for character in text:
        if character.lower() in vowels:
            ubby_text += 'ub' + character.lower()
        else:
            ubby_text += character
    return ubby_text

def unubby_translator(ubby_text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    original_text = ''
    i = 0
    while i < len(ubby_text):
        if i+1 < len(ubby_text) and ubby_text[i:i+2].lower() == 'ub' and ubby_text[i+2] in vowels:
            original_text += ubby_text[i+2]
            i += 3
        else:
            original_text += ubby_text[i]
            i += 1
    return original_text