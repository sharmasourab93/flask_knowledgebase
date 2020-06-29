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
# Logger Modules
from log.log_configurator import LogConfigurator


LogConfigurator.setup_logging()
logger = LogConfigurator.get_logger(__name__)


@flask_app.route("/", methods=['GET'])
def index():
    """To Get all the entries in DB"""
    logger.info("To Get all the entries in DB from {0}"
                .format(__name__))
    if current_user.is_authenticated:
        result = Dictionary.query.all()
        
        if len(result) == 0:
            message = "Entry Not  Found"
            logger.critical("{0} at {1}".format(message, __name__))
            return make_response(jsonify(message), 404)
        
        new_result = [{"id": i.id,
                       "word": i.word,
                       "meaning": i.meaning}
                      for i in result]
        logger.debug("All Items: Result {0}".format(new_result))
        return jsonify(new_result)
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/<id>", methods=['GET'])
def get_id(num: int):
    """To Get Entry by Unique ID"""
    logger.info("To Get Entry by Unique ID from {0}"
                .format(__name__))
    if current_user.is_authenticated:
        result = Dictionary.query. \
            filter(Dictionary.id == num).first()
        
        if not result:
            return make_response(jsonify("Entry Not found"),
                                 404)
        
        num, word, meaning = result.id, result.word, result.meaning
        result = {"id": num, "word": word, "meaning": meaning}
        logger.debug("Result for id: {0} is {1}".format(num, result))
        return jsonify(result)
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/by_word/<word>", methods=['GET'])
def get_by_word(word: str):
    """To get Entry by Unique Word"""
    logger.info("To get Entry by Unique Word from {0}"
                .format(__name__))
    if current_user.is_authenticated:
        result = Dictionary.query.filter(Dictionary.word == word).first()
        if result is None:
            message = "No Entry Found"
            return make_response(jsonify(message), 404)
        
        word, meaning = result.word, result.meaning
        
        result = {"word": word, "meaning": meaning}
        logger.debug("Result for word: {0} is {1}".format(word, result))
        return jsonify(result)
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/add/", methods=["POST"])
def insert_key_value():
    """To Insert/POST an Entry in DB"""
    logger.info("To get Entry by Unique Word from {0}"
                .format(__name__))
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
            logger.debug("Insertion Done. Redirecting to index")
            return redirect(url_for('index'))
        
        logger.critical("Entry Exists")
        return make_response(jsonify("Entry Exists"), 409)
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


@flask_app.route("/change/", methods=["PUT"])
def change_value():
    """To Alter the a value"""
    logger.info("To Alter the a value from {0}"
                .format(__name__))
    if current_user.is_authenticated:
        items = request.get_json()
        query = Dictionary.query \
            .filter(Dictionary.word == items['word']).first()
        query.meaning = items['meaning']
        db.session.commit()
        logger.debug("Updation Done. Redirecting to index")
        return redirect(url_for('index'))
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
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
            logger.debug("Deletion Done. Redirecting to index")
        except UnmappedInstanceError:
            message = "No Entry Found"
            logger.critical(message)
            return make_response(jsonify(message), 404)
        
        return redirect(url_for('index'))
    else:
        logger.warning("Current user Not Logged in. "
                       "Current User {0}".format(current_user))
        return make_response("Not allowed. "
                             "Login to access resources.",
                             401)


# Flask Register on the backend
@flask_app.route("/register", methods=['POST'])
def register():
    if current_user.is_authenticated:
        message = "You cannot register while logged in"
        logger.warning(message)
        return make_response(message,
                             405)
    
    else:
        items = request.get_json()
        creds = User.query \
            .filter(User.user == items['user']).first()
        if creds is not None:
            logger.warning("User exists")
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
    logger.info("Registration Successful. "
                "Login creds now available.\n{0}".format(items))
    return make_response("{0} is now registered. "
                         "Please Login with the "
                         "registered credentials."
                         .format(items['user']), 200)


# Flask Login on the backend
@flask_app.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        logger.debug("Redirecting to Index if authenticated.")
        return redirect(url_for('index'))
    
    items = request.get_json()
    
    uid, pwd = items['user'], items['password']
    cred = User.query.filter(User.user == uid).first()
    if cred is not None:
        hashed_pwd = bcrypt.check_password_hash(cred.password, pwd)
    else:
        logger.critical("User Not Registered")
        return make_response("User not registered", 401)
    
    if cred and hashed_pwd:
        login_user(cred, remember=True)
        logger.info("Login Successful.")
        return make_response("Login Successful.", 200)
    else:
        logger.warning("Invalid Credentials {0}".format(items))
        return make_response("Invalid Credentials! "
                             "Please try again",
                             401)


# Flask Log out
@flask_app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    logger.info("Logout Successful.")
    return make_response("User Logged Out.", 204)


@flask_app.route("/loggedin", methods=["GET"])
def logged_in():
    """Who is logged in?"""
    logger.info("Active Session Information")
    if current_user.is_authenticated:
        logger.info("User Logged in: {0}".format(current_user.user))
        return make_response(jsonify({"user": current_user.user}), 200)
    else:
        return make_response("No User logged in!", 200)
