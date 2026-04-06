from extensions import db

class Note(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    subject= db.Column(db.String(100), nullable=False)
    score= db.Column(db.Float, nullable=False)
    student_id= db.Column(db.Integer, db.ForeignKey('student.id'))
    student= db.relationship('Student', backref='notes')
