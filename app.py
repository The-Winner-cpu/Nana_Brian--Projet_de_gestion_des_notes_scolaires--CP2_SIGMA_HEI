from flask import Flask
from config import Config
from extensions import db, login_manager
from models.student import Student
from models.note import Note

app= Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view= "login"

from models.user import User
from controllers.auth_controller import register, login
from controllers.dashboard_controller import dashboard
from controllers.note_controller import add_note, list_notes, edit_note, delete_note, calculate_averages, ranking, performance_chart, generate_pdf, my_notes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.add_url_rule('/register', view_func= register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func= login, methods=['GET', 'POST'])
app.add_url_rule('/dashboard', view_func= dashboard)
app.add_url_rule('/add-note', view_func= add_note, methods=['GET', 'POST'])
app.add_url_rule('/notes', view_func= list_notes)
app.add_url_rule('/edit-note/<int:note_id>', view_func= edit_note, methods= ['GET', 'POST'])
app.add_url_rule('/delete-note/<int:note_id>', view_func= delete_note)
app.add_url_rule('/averages', view_func= calculate_averages)
app.add_url_rule('/ranking', view_func= ranking)
app.add_url_rule('/chart', view_func= performance_chart)
app.add_url_rule('/pdf/<int:student_id>', view_func= generate_pdf)
app.add_url_rule('/my-notes', view_func= my_notes)

from flask import render_template
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug= True, use_reloader= False)