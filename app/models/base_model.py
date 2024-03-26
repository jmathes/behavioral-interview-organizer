from app import db

Column = db.Column
Integer = db.Integer
String = db.String
ForeignKey = db.ForeignKey


class Model(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
