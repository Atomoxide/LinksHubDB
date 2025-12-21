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

@app.route('/api/get_data', methods=['GET'])
def get_data():
    items = query_db('select item_id, item_name, item_description, item_url, category_name, subcategory_name from item join subcategory on item.subcategory_id = subcategory.subcategory_id join category on subcategory.category_id = category.category_id')
    items_list = [dict(item) for item in items]
    concat_data = dict()
    for item in items_list:
        category = item.pop('category_name')
        subcategory = item.pop('subcategory_name')
        if category not in concat_data:
            concat_data[category] = dict()
        if subcategory not in concat_data[category]:
            concat_data[category][subcategory] = list()
        concat_data[category][subcategory].append(item)
    return jsonify(concat_data), 200

@app.route('/api/get_data_raw', methods=['GET'])
def get_data_raw():
    items = query_db('select item_id as id, item_name as name, item_description as description, item_url as url, category_name as category, subcategory_name as subcategory from item join subcategory on item.subcategory_id = subcategory.subcategory_id join category on subcategory.category_id = category.category_id')
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

@app.route('/api/get_channel', methods=['GET'])
def get_channels():
    channels = query_db('select meta_content from meta where meta_name = ?', ['channels'], one=True)
    if channels is None:
        return {"status": "Not Found"}, 404
    return {"channels": channels['meta_content']}, 200

@app.route('/api/get_subcategories', methods=['GET'])
def get_subcategories():
    subcategories = query_db('select subcategory_name as name, subcategory_description as description from subcategory')
    return jsonify({dict(sub)["name"]: dict(sub)["description"] for sub in subcategories}), 200

@app.route('/api/get_i18n_ZH', methods=['GET'])
def get_localization():
    localizations = query_db('select label, zh from local')
    return jsonify({dict(loc)["label"]: dict(loc)["zh"] for loc in localizations}), 200

## POST Methods
@app.route('/api/add_data', methods=['POST'])
def add_data():
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

@app.route('/api/update_data', methods=['POST'])
def update_data():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    item_id = data.get('item_id')
    item_name = data.get('item_name')
    item_description = data.get('item_description')
    item_url = data.get('item_url')
    subcategory_id = data.get('subcategory_id')
    if item_id is None or item_name is None or item_description is None or item_url is None or subcategory_id is None:
        return {"status": "Bad Request"}, 400
    query_db('update item set item_name = ?, item_description = ?, item_url = ?, subcategory_id = ? where item_id = ?', [item_name, item_description, item_url, subcategory_id, item_id])
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

@app.route('/api/update_channel', methods=['POST'])
def update_channels():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    channels = data.get('channels')
    if channels is None:
        return {"status": "Bad Request"}, 400
    query_db('update meta set meta_content = ? where meta_name = ?', [channels, 'channels'])
    return {"status": "Success"}, 200

@app.route('/api/add_subcategory', methods=['POST'])
def add_subcategory():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    subcategory_name = data.get('subcategory_name')
    subcategory_description = data.get('subcategory_description')
    category_id = data.get('category_id')
    if subcategory_name is None or subcategory_description is None or category_id is None:
        return {"status": "Bad Request"}, 400
    query_db('insert into subcategory (subcategory_name, subcategory_description, category_id) values (?, ?, ?)', [subcategory_name, subcategory_description, category_id])
    return {"status": "Success"}, 200

@app.route('/api/add_i18n_ZH', methods=['POST'])
def add_localization():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    label = data.get('label')
    zh = data.get('zh')
    if label is None or zh is None:
        return {"status": "Bad Request"}, 400
    query_db('insert into local (label, zh) values (?, ?)', [label, zh])
    return {"status": "Success"}, 200

@app.route('/api/update_i18n_ZH', methods=['POST'])
def update_localization():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    label = data.get('label')
    zh = data.get('zh')
    if label is None or zh is None:
        return {"status": "Bad Request"}, 400
    query_db('update local set zh = ? where label = ?', [zh, label])
    return {"status": "Success"}, 200

## Delete Methods
@app.route('/api/delete_data', methods=['DELETE'])
def delete_data():
    authorized = authorize(request=request)
    if not authorized: return {"status": "Unauthorized"}, 401
    data = request.get_json()
    item_id = data.get('item_id')
    if item_id is None:
        return {"status": "Bad Request"}, 400
    query_db('delete from item where item_id = ?', [item_id])
    return {"status": "Success"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)