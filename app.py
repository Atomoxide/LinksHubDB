import string
import random
import time
from datetime import datetime
from flask import Flask, g
from functools import wraps
import sqlite3
from flask import *
from hashlib import sha256


app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect('db/db.sqlite')
        db.row_factory = sqlite3.Row
        setattr(g, '_database', db)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.execute(query, args)
    rows = cursor.fetchall()
    db.commit()
    cursor.close()
    if rows:
        if one: 
            return rows[0]
        return rows
    return None

def authorize(request: Request):
    admin_password_hash = request.headers.get("Admin-Password-Hash")
    admin_name = request.headers.get("Admin-Name")
    if admin_password_hash is None or admin_name is None: return False
    admin = query_db('select * from admin where admin_name = ?', [admin_name], one=True)
    if admin is None:
        return False
    if admin['admin_password_hash'] != admin_password_hash:
        return False
    return True

# API Routes

## GET Methods
@app.route('/api/test', methods=['GET'])
def get_connection():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    return {"status": "Success"}, 200

@app.route('/api/get_items', methods=['GET'])
def get_items():
    # authorized = authorize(request=request)
    # if not authorized: return {"status": "Unauthorized"}, 401
    items = query_db('select item_id, item_name, item_description, item_url, category_name, subcategory_name from item join subcategory on item.subcategory_id = subcategory.subcategory_id join category on subcategory.category_id = category.category_id')
    items_list = [dict(item) for item in items]
    return jsonify(items_list), 200

@app.route('/api/get_version', methods=['GET'])
def get_version():
    version = query_db('select meta_content from meta where meta_name = ?', ['version'], one=True)
    if version is None:
        return {"status": "Not Found"}, 404
    return {"version": version['meta_content']}, 200

@app.route('/api/get_version_logo', methods=['GET'])
def get_version_logo():
    version_logo = query_db('select meta_content from meta where meta_name = ?', ['version_logo'], one=True)
    if version_logo is None:
        return {"status": "Not Found"}, 404
    return {"version_logo": version_logo['meta_content']}, 200

@app.route('/api/get_announcement', methods=['GET'])
def get_announcement():
    announcement = query_db('select meta_content from meta where meta_name = ?', ['announcement'], one=True)
    if announcement is None:
        return {"status": "Not Found"}, 404
    return {"announcement": announcement['meta_content']}, 200

@app.route('/api/get_channels', methods=['GET'])
def get_channels():
    channels = query_db('select meta_content from meta where meta_name = ?', ['channels'], one=True)
    if channels is None:
        return {"status": "Not Found"}, 404
    return {"channels": channels['meta_content']}, 200

## POST Methods
@app.route('/api/add_item', methods=['POST'])
def add_item():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    item_name = data.get('item_name')
    item_description = data.get('item_description')
    item_url = data.get('item_url')
    subcategory_id = data.get('subcategory_id')
    if item_name is None or item_description is None or item_url is None or subcategory_id is None:
        return {"status": "Bad Request"}, 400
    query_db('insert into item (item_name, item_description, item_url, subcategory_id) values (?, ?, ?, ?)', [item_name, item_description, item_url, subcategory_id])
    return {"status": "Success"}, 200

@app.route('/api/update_version', methods=['POST'])
def update_version():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    version = data.get('version')
    if version is None:
        return {"status": "Bad Request"}, 400
    query_db('update meta set meta_content = ? where meta_name = ?', [version, 'version'])
    return {"status": "Success"}, 200

@app.route('/api/update_version_logo', methods=['POST'])
def update_version_logo():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    version_logo = data.get('version_logo')
    if version_logo is None:
        return {"status": "Bad Request"}, 400
    query_db('update meta set meta_content = ? where meta_name = ?', [version_logo, 'version_logo'])
    return {"status": "Success"}, 200

@app.route('/api/update_announcement', methods=['POST'])
def update_announcement():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    announcement = data.get('announcement')
    if announcement is None:
        return {"status": "Bad Request"}, 400
    query_db('update meta set meta_content = ? where meta_name = ?', [announcement, 'announcement'])
    return {"status": "Success"}, 200

@app.route('/api/update_channels', methods=['POST'])
def update_channels():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    channels = data.get('channels')
    if channels is None:
        return {"status": "Bad Request"}, 400
    query_db('update meta set meta_content = ? where meta_name = ?', [channels, 'channels'])
    return {"status": "Success"}, 200

if __name__ == "__main__":
    app.run(debug=True)