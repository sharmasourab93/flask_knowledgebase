# Core Flask App Modules
from flask import request, redirect, url_for
from flask import make_response, jsonify
# Flask App modules
from flask_kb import flask_app, db, bcrypt
from flask_kb.models.dict_table import Dictionary
from flask_kb.models.users import User
# Flask Login Components
from flask_login import login_user, current_user, logout_user
#To Handle UnmappedInstanceError
from sqlalchemy.orm.exc import UnmappedInstanceError
# To import BrowseMeaning in eng_dictionary package
from dictionary import BrowseMeaning


@flask_app.route("/", methods=['GET'])
def index():
    """To Get all the entries in DB"""
    if current_user.is_authenticated:
        result = Dictionary.query.all()
        
        if len(result) == 0:
            message = "Entry Not  Found"
            return make_response(jsonify(message), 404)
        
        new_result = [{"id": i.id,
                       "word": i.word,
                       "meaning": i.meaning}
                      for i in result]
        return jsonify(new_result)
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/<id>", methods=['GET'])
def get_id(id_: int):
    """To Get Entry by Unique ID"""
    if current_user.is_authenticated:
        result = Dictionary.query. \
            filter(Dictionary.id == id_).first()
        
        if not result:
            return make_response(jsonify("Entry Not found"),
                                 404)
        
        id_, word, meaning = result.id, result.word, result.meaning
        
        return jsonify({"id": id_,
                        "word": word,
                        "meaning": meaning})
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/by_word/<word>", methods=['GET'])
def get_by_word(word: str):
    """To get Entry by Unique Word"""
    if current_user.is_authenticated:
        result = Dictionary.query.filter(Dictionary.word == word).first()
        if result is None:
            return make_response(jsonify("No Entry Found"), 404)
        
        id_, word, meaning = result.id, result.word, result.meaning
        
        return jsonify({"id": id_,
                        "word": word,
                        "meaning": meaning})
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/add/", methods=["POST"])
def insert_key_value():
    """To Insert/POST an Entry in DB"""
    if current_user.is_authenticated:
        items = request.get_json()
        query = Dictionary.query \
            .filter(Dictionary.word == items['word']).first()
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
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/change/", methods=["PUT"])
def change_value():
    """To Alter the a value"""
    if current_user.is_authenticated:
        items = request.get_json()
        query = Dictionary.query \
            .filter(Dictionary.word == items['word']).first()
        query.meaning = items['meaning']
        db.session.commit()
        
        return redirect(url_for('index'))
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/<id>", methods=['DELETE'])
def delete_by_id(id_: int):
    """To Delete an Entry"""
    if current_user.is_authenticated:
        query = Dictionary.query \
            .filter(Dictionary.id == id_).first()
        
        try:
            db.session.delete(query)
            db.session.commit()
        except UnmappedInstanceError:
            return make_response(jsonify("No Entry Found"), 404)
        
        return redirect(url_for('index'))
    else:
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


# Flask Register on the backend
@flask_app.route("/register", methods=['POST'])
def register():
    if current_user.is_authenticated:
        return make_response("You cannot register while logged in",
                             405)
    
    else:
        items = request.get_json()
        creds = User.query \
            .filter(User.user == items['user']).first()
        if creds is not None:
            return make_response("User exists. "
                                 "Please login instead.",
                                 409)
    
    items = request.get_json()
    pwd = items['password']
    hashed_pwd = bcrypt.generate_password_hash(pwd).decode()
    creds = User(user=items['user'],
                 email=items['email'],
                 password=hashed_pwd)
    
    db.session.add(creds)
    db.session.commit()
    return make_response("{0} is now registered. "
                         "Please Login with the "
                         "registered credentials."
                         .format(items['user']), 200)


# Flask Login on the backend
@flask_app.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    items = request.get_json()
    
    uid, pwd = items['user'], items['password']
    cred = User.query.filter(User.user == uid).first()
    if cred is not None:
        hashed_pwd = bcrypt.check_password_hash(cred.password, pwd)
    else:
        return make_response("User not registered", 401)
    
    if cred and hashed_pwd:
        login_user(cred, remember=True)
        return make_response("Login Successful.", 200)
    else:
        return make_response("Invalid Credentials! "
                             "Please try again",
                             401)


# Flask Log out
@flask_app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return make_response("User Logged Out.", 204)


@flask_app.route("/loggedin", methods=["GET"])
def logged_in():
    if current_user.is_authenticated:
        return make_response(jsonify({"user": current_user.user}), 200)
    else:
        return make_response("No User logged in!", 200)
