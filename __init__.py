import sys, os, random, string
os.path.abspath("Flask")
sys.path.append(os.path.abspath("Flask"))

from flask import Flask, render_template, url_for, flash, redirect, session
from forms import UrlForm
from db import create_SUrl, getLongUrlFromDatabase, checkIfExistInDatabase, getShortUrlFromDatabase, init_db, getSizeOfURL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.root_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home')
    def home():
        form = UrlForm()
        if form.validate_on_submit():
            boolIsExist = checkIfExistInDatabase(form['urlFromUser'].data)
            if boolIsExist is False:
                shortUrl = randomStringDigits(5)
                create_SUrl(shortUrl, form['urlFromUser'].data)
                flash('You are enter a good URL: ' +  form['urlFromUser'].data)
                session['shortUrl'] = shortUrl
                return redirect(url_for('shortener'))
            else:
                shortUrl = getShortUrlFromDatabase(form['urlFromUser'].data)
                session['shortUrl'] = shortUrl
                return redirect(url_for('shortener'))
        return render_template('home.html', title='home', form=form)


    @app.route('/shortener', methods=['GET','POST'])
    def shortener():
        shortUrl = session.get('shortUrl', None)
        return render_template('shortener.html', shortUrl = shortUrl)


    @app.route('/<urlToCheck>')
    def checkRoute(urlToCheck):
	       longUrl= getLongUrlFromDatabase(urlToCheck)
	       if longUrl is None:
		             print ('No such short URL')
	       else:
                     return redirect(longUrl, code = 302)

    @app.route('/stats', methods=['GET','POST'])
    def stats():
        sizeOfUrl = getSizeOfURL()
        return render_template('stats.html',title='stats', sizeOfUrl=sizeOfUrl)


    #Generate a random string of letters and digits
    def randomStringDigits(stringLength=5):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    from . import db
    db.init_app(app)

    return app
