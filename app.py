from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

# import cleanup
# import tokenize
# import word_count
# import sample
# import sentence
from frequency import Histogram

#with heroku
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TweetGen')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

histograms = db.histograms
favorites = db.favorites

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    ''' show all histograms '''
    return render_template('index.html', histograms=histograms.find())


@app.route('/histograms', methods=['POST', 'GET'])
def histogram_saved():
    text = request.form.get('source_text')
    histogram = Histogram(str(text))
    new_histogram = {
        'histogram': histogram.histogram,
        'types': histogram.total_types,
        'tokens': histogram.total_tokens,
        'random_words': histogram.sample_by_frequency(10),
        'markov_dict': histogram.markov_chain
    }
    # histogram_id = histograms.insert_one(new_histogram).inserted_id
    histograms.insert_one(new_histogram)
    return redirect(url_for('index'))


@app.route('/create')
def create_histogram():
    ''' form to create a generator '''
    return render_template('sourcetext_form.html', histogram={})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
