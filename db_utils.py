import psycopg2
from psycopg2.extras import RealDictCursor, NamedTupleCursor
import json
from json import JSONEncoder
import datetime
from datetime import date
import os

db_host = 'localhost'
db_name = 'blogging'
db_user = 'postgres'
db_pass = 'Click05$'

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
    except:
        print("Unable to connect to the database")
    return conn

def list_stories(limit=5, offset=0):
    result = []

    query = "SELECT * FROM story LIMIT {} OFFSET {}"
    query = query.format(limit, offset)

    conn = make_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()

    return data


def add(title, description, body, tags=None):
    result = []
    conn = make_conn()
    id = None
    query = ''' INSERT INTO story 
                        (title, description, body, tags) 
                VALUES  (%s, %s, %s, %s)
                RETURNING id 

    '''
    cursor = conn.cursor()
    cursor.execute(query, (title, description, body, tags) )
    data =  cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return data

def get(id):

    query = ''' SELECT * FROM  story WHERE id = {} '''
    query = query.format(id)   

    conn = make_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)

    data = cursor.fetchone()
    conn.close()

    return data  

def update(id, status):
    
    query = ''' UPDATE story SET published={} WHERE id={}'''
    query = query.format(status, id)

    conn = make_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()