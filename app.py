from flask import Flask, render_template, request
import cleanup
import tokenize
import word_count
import sample
import sentence

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
