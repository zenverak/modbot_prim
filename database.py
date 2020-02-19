import sqlite3
from datetime import datetime

import globals

dbConn = None


def init():
    global dbConn
    dbConn = sqlite3.connect(globals.database_name)
    c = dbConn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS posts(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_name char(30),
                    author_id INTEGER,
                    postid INTEGER,
                    post_time TIMESTAMP,
                    channel_name char(30),
                    channel_id INTEGER,
                    override INTEGER
                    
              )
            ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS warns(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_name char(30),
                    author_id INTEGER,
                    warn_type char(40),
                    warn_date TIMESTAMP,
                    post char(2100),
              )
            ''')
    dbConn.commit()
            

            
init()


def insert_post(message):
    c = dbConn.cursor()
    try:
        c.execute('''
       insert into posts(author_name, author_id, postid, post_time,channel_name, channel_id, override) values(?,?,?,?,?,?,?)
      ''',(message.author.name, message.author.id, message.id, message.created_at,message.channel.name, message.channel.id,0)
      )
    dbConn.commit()
    
def insert_warn(message, type_):
    c = dbConn.cursor()
    try:
        c.execute('''insert ito warns(author_name, author_id,warn_type, warn_date, post) values(?,?,?,?,?)''',(message.author.name,message.author.id,type_,message.created_at,message.content))
    dbConn.commit()


def get_warn_total(user):
    c = dbConn.cursor()
    try:
        c.execute('''select count(*) from warns where author_id = ?''',(user.id))
        return c.fetchone()[0]
    except:
        return False
