from flask import render_template
from flask_login import login_required, current_user

@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return render_template('student_dashboard.html')