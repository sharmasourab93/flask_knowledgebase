# Core Flask App Modules
from flask import request, redirect, url_for
from flask import make_response, jsonify
# Flask App modules
from flask_kb import flask_app
from flask_kb.models.dict_table import Dictionary
from flask_kb import db
#To Handle UnmappedInstanceError
from sqlalchemy.orm.exc import UnmappedInstanceError
# To import BrowseMeaning in eng_dictionary package
from dictionary import BrowseMeaning


@flask_app.route("/", methods=['GET'])
def index():
    """To Get all the entries in DB"""
    result = Dictionary.query.all()
    
    if len(result) == 0:
        status_code = 404
        message = "Entry Not  Found"
        return make_response(jsonify(message), status_code)
    
    new_result = [{"id": i.id, "word": i.word, "meaning": i.meaning}
                  for i in result]
    return jsonify(new_result)


@flask_app.route("/<id>", methods=['GET'])
def get_id(id: int):
    """To Get Entry by Unique ID"""
    result = Dictionary.query.filter(Dictionary.id == id).first()
    if not result:
        status_code = 404
        return make_response(jsonify("Entry Not found"), status_code)
    
    id, word, meaning = result.id, result.word, result.meaning
    
    return jsonify({"id": id,
                    "word": word,
                    "meaning": meaning})


@flask_app.route("/by_word/<word>", methods=['GET'])
def get_by_word(word: str):
    """To get Entry by Unique Word"""
    result = Dictionary.query.filter(Dictionary.word == word).first()
    if result is None:
        return make_response(jsonify("No Entry Found"), 404)
    
    id, word, meaning = result.id, result.word, result.meaning
    
    return jsonify({"id": id,
                    "word": word,
                    "meaning": meaning})


@flask_app.route("/add/", methods=["POST"])
def insert_key_value():
    """To Insert/POST an Entry in DB"""
    items = request.get_json()
    query = Dictionary.query.filter(Dictionary.word == items['word']).first()
    if query is None:
        dict_ = BrowseMeaning()
        mean = dict_.search(items['word'])
        
        query = Dictionary(word=items['word'],
                           meaning=mean
                           )
        db.session.add(query)
        db.session.commit()
        return redirect(url_for('index'))
    
    return make_response(jsonify("Entry Exists"), 409)


@flask_app.route("/change/", methods=["PUT"])
def change_value():
    """To Alter the a value"""
    items = request.get_json()
    query = Dictionary.query.filter(Dictionary.word == items['word']).first()
    query.meaning = items['meaning']
    db.session.commit()
    
    return redirect(url_for('index'))


@flask_app.route("/<id>", methods=['DELETE'])
def delete_by_id(id: int):
    """To Delete an Entry"""
    query = Dictionary.query.filter(Dictionary.id == id).first()
    
    try:
        db.session.delete(query)
        db.session.commit()
    except UnmappedInstanceError:
        return make_response(jsonify("No Entry Found"), 404)
    
    return redirect(url_for('index'))
