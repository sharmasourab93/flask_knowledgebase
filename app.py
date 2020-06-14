"""
Flask Application
The application should be able to do the following
over HTTP Protocols namely `GET`, `POST`, `PUT` and `DELETE`:

    1. Get all the Knowledge Items
    2. Get a Knowledge Item based on UID
    3. Get a Knowledge Item based on a Row Value
    4. Insert Values
    5. Alter Values
    6. Delete Values
    
    
This file also holds the components which initializes Database table.
Configurations are handled by `load_configs.py` which seeks manual
inputs from `config.yaml`
"""
from flask import Flask, request, redirect, url_for
from flask import make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from load_configs import CONN_STRING
from sqlalchemy.orm.exc import UnmappedInstanceError
from dictionary import BrowseMeaning


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(flask_app)


class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    word = db.Column(db.String(50), nullable=False)
    meaning = db.Column(db.String(100))
    
    def __str__(self):
        return jsonify({"id": self.id,
                "word": self.word,
                "meaning": self.meaning})


@flask_app.route("/", methods=['GET'])
def index():
    """To Get all the entries in DB"""
    result = Dictionary.query.all()
    
    if len(result) == 0:
        status_code = 404
        message = "No Entries Found"
        return make_response(jsonify(message), status_code)
    
    new_result = [{"id": i.id, "word": i.word, "meaning": i.meaning}
                  for i in result]
    return jsonify(new_result)


@flask_app.route("/<id>", methods=['GET'])
def get_id(id: int):
    """To Get Entry by Unique ID"""
    result = Dictionary.query.filter(Dictionary.id==id).first()
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
    result = Dictionary.query.filter(Dictionary.word==word).first()
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
    query = Dictionary.query.filter(Dictionary.word==items['word']).first()
    if query is None:
        dict_ = BrowseMeaning()
        mean = dict_.search(items['word'])
    
        query = Dictionary(word=items['word'],
                           meaning=mean[:100]
                           )
        db.session.add(query)
        db.session.commit()
        return redirect(url_for('index'))
    
    return make_response(jsonify("Entry Exists"), 409)


@flask_app.route("/change/", methods=["PUT"])
def change_value():
    """To Alter the a value"""
    items = request.get_json()
    query = Dictionary.query.filter(Dictionary.word==items['word']).first()
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
    

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
