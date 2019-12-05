from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

# import cleanup
# import tokenize
# import word_count
# import sample
# import sentence
from frequency import *
# from werkzeug.utils import secure_filename
#
# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = {'txt', ''}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#with heroku
# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TweetGen')
# client = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()

client = MongoClient()
db = client.TweetGen

generators = db.generators
favorites = db.favorites

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    ''' show all histograms '''
    return render_template('index.html', generators=generators.find(), title='Tweet Generator')


@app.route('/generator', methods=['POST', 'GET'])
def histogram_saved():
    text = request.form.get('source_text')
    name = request.form.get('name')
    desc = request.form.get('desc')

    generator = Histogram(str(text))
    new_generator = {
        'name': name,
        'description': desc,
        'word_list': generator.word_list,
        'histogram': generator.histogram,
        'types': generator.total_types,
        'tokens': generator.total_tokens,
        'random_words': bulk_sample(generator.histogram, generator.total_tokens, 10),
        'markov_dict': generator.markov_chain,
        'random_sentence': random_sentence(generator.markov_chain)
    }
    generator_id = generators.insert_one(new_generator).inserted_id
    return redirect(url_for('show_generator', generator_id=generator_id))


@app.route('/generator/<generator_id>')
def show_generator(generator_id):
    generator = generators.find_one({'_id': ObjectId(generator_id)})
    generator['random_words'] = bulk_sample(generator['histogram'], generator['tokens'], 10)
    generator['random_sentence'] = random_sentence(generator['markov_dict'])
    return render_template('show_generator.html', generator=generator, title=generator['name'])


@app.route('/generator/<generator_id>/edit')
def edit_generator(generator_id):
    generator = generators.find_one({'_id': ObjectId(generator_id)})
    return render_template('edit_form.html', generator=generator, title='Edit Generator')


@app.route('/generator/<generator_id>/delete', methods=['POST'])
def remove_generator(generator_id):
    generators.delete_one({'_id': ObjectId(generator_id)})
    return redirect(url_for('index'))


@app.route('/create')
def create_histogram():
    ''' form to create a generator '''
    return render_template('sourcetext_form.html', generator={})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
