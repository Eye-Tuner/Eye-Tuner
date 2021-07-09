from app import db


class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(8))
    password = db.Column(db.String(200), nullable=False)  # hashed field

    def __repr__(self):
        return '<User: %s>' % self.id
