import os
import flask
import json
from flask import Flask, render_template, redirect, session, g, url_for, abort, flash
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

# configuration

password = os.environ['password']
libera_url = "54.164.158.211"

# create application object
app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'libera_db'
app.config['MONGO_URI'] = "mongodb://paul:" + password + "@" + libera_url + "/libera_db"

topic_dict = {0:'Education',1:'Algorithms/Models',2:'Deep Learning',
		3:'Storytelling with Data', 4:'Data Science Programming', 5:'Data Mining and Databases',6:'Statistics', 7:'Data Visualization', 8:'Big Data', 9:'Data Science Central'}

mongo = PyMongo(app)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/layout')
def layout():
	return render_template('layout.html')
@app.route('/', methods=['GET', 'POST'])
def landing_page():
	        return render_template('landing_page.html')
@app.route('/about')
def about():
	return render_template('landing_page.html')
@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Log in successful')
			return redirect(url_for('generate_blogroll'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Log out successful')
	return redirect(url_for('landing_page'))

@app.route('/register', methods=['GET','POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'admin':
			error='Username already taken'
		elif request.form['password'] != request.form['confirmPassword']:
			error='Passwords do not match'
		else:
			return redirect(url_for('interest_form'))
	return render_template('sign_up.html', error=error)

@app.route('/interest_form', methods=['GET', 'POST'])
def interest_form():
	collection = mongo.db.scraped_blogs
	topics = collection.find( {"cluster": { '$exists': True} } ).distinct("cluster")
	return render_template('interest.html', topics = topics, topic_dict=topic_dict)


@app.route('/blogroll', methods=['GET', 'POST'])
def generate_blogroll():
	session['logged_in'] = True
	if not session.get('logged_in'):
		redirect(url_for('landing_page'))
	else:
		interests = []
		for k,v in request.form.items():
			interests.append(int(v))
		collection = mongo.db.scraped_blogs
		interest_dict = {}
		if len(interests)==0:
			interest = [2,7,8,5]	
		for interest in interests:
			starter_urls = collection.aggregate( [{'$match':{'quality':True, 'cluster':interest}}, {'$sample' :{'size': 2}}])
			url1 = starter_urls.next()
			url2 = starter_urls.next()
			interest_dict[interest] = {'url1': url1['url'], 'url2': url2['url']}	
		return render_template('feed.html', interests=interest_dict, topic_dict=topic_dict)
	
@app.route('/next_entry', methods=['GET','POST'])
def next_entry():
	data = flask.request.get_json()
	cluster = data['cluster']
	collection = mongo.db.scraped_blogs
	blog = collection.aggregate([ {'$match':{'quality':True, 'cluster':cluster}},{ '$sample': { 'size': 1 }} ]).next()
	output = {'url' : blog['url']}
	return flask.jsonify(output)

@app.route('/account', methods=['GET', 'POST'])
def account():
	if not session.get('logged_in'):
		session['logged_in'] = True
	collection = mongo.db.scraped_blogs
	interests = [2,7,8,5]
	interest_dict = {}
	for interest in interests:
		starter_urls = collection.aggregate( [{'$match':{'quality':True, 'cluster':interest}}, {'$sample' :{'size': 2}}])
		url1 = starter_urls.next()
		url2 = starter_urls.next()
		interest_dict[interest] = {'url1': url1['url'], 'url2': url2['url']}
	return render_template('feed.html', interests=interest_dict, topic_dict=topic_dict)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgot_password():
	return render_template('login.html')

if __name__ == '__main__':
        app.run(debug=True)


