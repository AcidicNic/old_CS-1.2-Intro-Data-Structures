from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

from histogram import *

# from werkzeug.utils import secure_filename
#
# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = {'txt', ''}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TweetGen')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

generators = db.generators
favorites = db.favorites

app = Flask(__name__)

# with open('source_text', 'r') as file:
#     main_source_text = file.read()


# histogram
main_source_text = histogram_file('source_text')
main_word_list = get_word_list(main_source_text)
main_histogram = get_histogram(main_word_list)
main_tokens = get_total_tokens(main_histogram)
main_types = unique_words(main_histogram)
main_markov = markov(main_word_list)

main_generator = {
    'name': "idk",
    'description': "test"
}


@app.route('/')
def main_gen():
    main_generator['random_words'] = bulk_sample(main_histogram, main_tokens, 10)
    main_generator['random_sentence'] = random_sentence(main_markov)
    return render_template('show_generator.html', generator=main_generator, title=main_generator['name'])


@app.route('/show_all', methods=['POST', 'GET'])
def show_all():
    ''' show all histograms '''
    gen_list = []
    for generator in generators.find():
        gen_list.append(generator['gen'])
    return render_template('index.html', generators=gen_list, title='Tweet Generator')


@app.route('/generator', methods=['POST', 'GET'])
def histogram_saved():
    text = request.form.get('source_text')
    name = request.form.get('name')
    desc = request.form.get('desc')

    generator = Histogram(str(text))
    new_generator = {
        'gen': {
            'name': name,
            'description': desc,
            'word_list': generator.word_list,
            'types': generator.total_types,
            'tokens': generator.total_tokens
        },
        'histogram': generator.histogram,
        'markov_dict': generator.markov_chain,
    }
    generator_id = generators.insert_one(new_generator).inserted_id
    return redirect(url_for('show_generator', generator_id=generator_id))


@app.route('/generator/<generator_id>')
def show_generator(generator_id):
    generator = generators.find_one({'_id': ObjectId(generator_id)})
    # generator['random_words'] = bulk_sample(generator['histogram'], generator['tokens'], 10)
    generator['random_sentence'] = random_sentence(generator['markov_dict'])
    return render_template('show_generator.html', generator=generator, title=generator['name'])


@app.route('/generator/<generator_id>/edit')
def edit_generator(generator_id):
    generator = generators.find_one({'_id': ObjectId(generator_id)})
    return render_template('edit_form.html', generator=generator, title='Edit Generator')


@app.route('/generator/<generator_id>', methods=['POST'])
def update_generator(generator_id):
    text = request.form.get('source_text')
    name = request.form.get('name')
    desc = request.form.get('desc')

    generator = Histogram(str(text))
    updated_generator = {
        'gen': {
            'name': name,
            'description': desc,
            'word_list': generator.word_list,
            'types': generator.total_types,
            'tokens': generator.total_tokens
        },
        'histogram': generator.histogram,
        'markov_dict': generator.markov_chain,
    }
    generators.update_one(
        {'_id': ObjectId(generator_id)},
        {'$set': updated_generator})
    return redirect(url_for('show_generator', generator_id=generator_id))


@app.route('/generator/<generator_id>/delete', methods=['POST'])
def remove_generator(generator_id):
    generators.delete_one({'_id': ObjectId(generator_id)})
    return redirect(url_for('show_all'))


@app.route('/create')
def create_histogram():
    ''' form to create a generator '''
    return render_template('sourcetext_form.html', generator={})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
