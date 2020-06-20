from flask_kb import db


class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    word = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    meaning = db.Column(db.String(1000))
    
    def __repr__(self):
        return f"Dictionary('{self.id}', '{self.word}','{self.meaning}')"
