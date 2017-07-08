import os
import flask
import json
from flask import Flask, render_template, redirect
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

# configuration

password = os.environ['password']
libera_url = "54.164.158.211"
x = 0
# create application object
app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'libera_db'
app.config['MONGO_URI'] = "mongodb://paul:" + password + "@" + libera_url + "/libera_db"

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def show_random_article():
	data = flask.request.get_json()
	if not data:
		data = {'index':0}
	x = data['index']
	collection = mongo.db.scraped_blogs
	blog = collection.find({'needs_hand_rating':True}).limit(1)[0]
	blog_id = blog['_id']
	output = {'url' : blog['url'], 'text' : blog['text']}
	result = jsonify({'result': output})
	return render_template('index.html', _id = blog_id, url=output['url'], text=output['text'])

@app.route('/update_entry', methods=['GET', 'POST'])
def update_entry():
	print('hello')
	data = flask.request.get_json()
	data = eval(data)
	collection = mongo.db.scraped_blogs
	collection.update_one({'url': data['link']},{ '$set': {'skipped': False, 'hand_reviewed' : True, 'needs_hand_rating':False, 'quality' : data['quality']}})
	return flask.jsonify(data)

@app.route('/skip_entry', methods=['GET','POST'])
def skip_entry():
	data = flask.request.get_json()
	data = eval(data)
	collection = mongo.db.scraped_blogs
	collection.update_one({'url': data['link']},{'$set': {'hand_reviewed' : True, 'needs_hand_rating':False, 'skipped':True}})
	return flask.jsonify(data)

@app.route('/next_entry', methods=['GET','POST'])
def next_entry():
	data = flask.request.get_json()
	x = data['index']
	collection = mongo.db.scraped_blogs
	blog = collection.find({'needs_hand_rating':True}).limit(1)[x]
	output = {'url' : blog['url'], 'text' : blog['text']}
	return flask.jsonify(output)

@app.route('/previous_entry', methods=['GET','POST'])
def previous_entry():
	data = flask.request.get_json()
	data = eval(data)
	previous_url = data['link']
	collection = mongo.db.scraped_blogs
	blog = collection.find({'url': previous_url})[0]
	output = {'url': blog['url'], 'text' : blog['text']}
	return flask.jsonify(output)
#@app.route('/test', methods = ['POST'])
#def update_article_is_quality():
#	backup = mongo.db.backup
#
# FLASH TEXT TO SAY UPDATE WORKED AND RELOAD

#@app.route('/test', methods = ['POST'])
#def update_article_is_not_quality():
#	backup = mongo.db.backup
#	
# FLASH TEXT TO SAY UPDATE WORKED AND RELOAD

if __name__ == '__main__':
	app.run(debug=True)
