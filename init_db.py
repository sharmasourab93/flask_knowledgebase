from app import db


def initialize_db():
    db.create_all()
    
    
if __name__ == '__main__':
    initialize_db()
