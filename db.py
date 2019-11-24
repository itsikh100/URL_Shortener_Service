import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def checkIfExistInDatabase(longUrl):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("select * from URL where longUrl = ?", [longUrl])
    data=cur.fetchall()
    if len(data)==0:
        return False
    else:
        return True


def create_SUrl(shorturl, longurl):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO URL (shortUrl, longUrl, modifyTime) VALUES (?, ?, ?)",
        (shorturl, longurl, datetime.now()))
    conn.commit()
    return cur.lastrowid

def getShortUrlFromDatabase(longUrl):
    conn = get_db()
    cur = conn.cursor()
    cur .execute("SELECT shortUrl from URL WHERE longUrl = ?", [longUrl])
    return str(cur.fetchone()[0])



def getLongUrlFromDatabase(shortUrl):
	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT longUrl from URL WHERE shortUrl = ?", [shortUrl])
	return str(cur.fetchone()[0])


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def getSizeOfURL():
    conn = get_db()
    cur = conn.cursor()
    counter =0
    cur.execute("SELECT * FROM URL")
    for row in cur.fetchall():
        counter = counter+1
    return counter       


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
