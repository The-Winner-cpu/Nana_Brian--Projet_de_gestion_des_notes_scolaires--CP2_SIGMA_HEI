from flask import render_template, request, redirect, send_file
from models.student import Student
from models.note import Note
from extensions import db
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask_login import current_user, login_required
import io

@login_required
def add_note():
    if current_user.role != 'admin':
        return "Accès refusé mon type !"
    if request.method == 'POST':
        student_name= request.form.get('student')
        subject= request.form.get('subject')
        score= float(request.form.get('score'))
        student= Student.query.filter_by(name= student_name).first()
        if not student:
            student= Student(name= student_name, user_id= current_user.id)
            db.session.add(student)
            db.session.commit()
        new_note = Note(
            subject= subject,
            score= score,
            student_id= student.id
        )
        db.session.add(new_note)
        db.session.commit()
        return redirect('/notes')
    return render_template('add_note.html')

@login_required
def list_notes():
    if current_user.role == 'admin':
        notes= Note.query.all()
    else:
        student= Student.query.filter_by(name= current_user.username).first()        
        if student:
            notes= student.notes
        else:
            notes= []
    return render_template('notes.html', notes= notes)

@login_required
def delete_note(note_id):
    if current_user.role != 'admin':
        return "Accès refusé mon type !"
    note= Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect('/notes')

@login_required
def edit_note(note_id):
    if current_user.role != 'admin':
        return "Accès refusé mon type !"
    note= Note.query.get(note_id)
    if request.method == 'POST':
        note.subject= request.form.get('subject')
        note.score= float(request.form.get('score'))
        db.session.commit()
        return redirect('/notes')
    return render_template('edit_note.html', note=note)

def calculate_averages():
    students= Student.query.all()
    results= []
    for student in students:
        notes= student.notes
        if notes:
            total= sum(note.score for note in notes)
            average= total / len(notes)
        else:
            average= 0
        results.append({ 'name': student.name, 'average': round(average, 2) })
    all_notes = Note.query.all()
    if all_notes:
        general_avg= sum(n.score for n in all_notes) / len(all_notes)
    else:
        general_avg= 0
    return render_template(
        'averages.html',
        results=results,
        general_avg=round(general_avg, 2)
    )

def ranking():
    students= Student.query.all()
    results= []
    for student in students:
        notes= student.notes
        if notes:
            total= sum(note.score for note in notes)
            average= total / len(notes)
        else:
            average= 0
        results.append({ 'name': student.name, 'average': round(average, 2) })

    results.sort(key= lambda x: x['average'], reverse= True)
    for i, student in enumerate(results):
        student['rank']= i+1
    return render_template('ranking.html', results= results)

@login_required
def performance_chart():
    if current_user.role != 'admin':
        return "Accès refusé mon type !"
    students= Student.query.all()
    names= []
    averages= []
    for student in students:
        notes= student.notes
        if notes:
            avg= sum(n.score for n in notes) / len(notes)
        else:
            avg= 0
        names.append(student.name)
        averages.append(avg)

    plt.figure()
    plt.bar(names, averages, color='green')
    plt.xlabel("Étudiants")
    plt.ylabel("Moyenne")
    plt.title("Performances des étudiants")
    chart_path= os.path.join('static', 'chart.png')
    full_path= os.path.join(os.getcwd(), chart_path)
    plt.savefig(full_path)
    plt.savefig(chart_path)
    plt.close()
    return render_template('chart.html')

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import send_file
import io
import os

def generate_pdf(student_id):
    student= Student.query.get(student_id)
    if current_user.role != 'admin' and student.name != current_user.username:
        return "Accès interdit mon type !"
    notes= student.notes
    buffer= io.BytesIO()
    pdf= canvas.Canvas(buffer, pagesize= A4)
    bg_path= os.path.join('static', 'header.png')
    full_bg_path= os.path.join(os.getcwd(), bg_path)
    pdf.drawImage(full_bg_path, 0, 0, width= 595, height= 842)
    x= 150
    y= 550
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, f"Nom de l'étudiant : {student.name}")
    y -= 30
    total= 0
    pdf.setFont("Helvetica", 14)
    pdf.drawString(x, y, f"Matières                               Notes")
    y -= 20
    total= 0
    pdf.setFont("Helvetica", 14)
    pdf.drawString(x, y, f" ")
    y -= 18
    total= 0
    pdf.setFont("Helvetica", 14)
    pdf.drawString(x, y, f" ")
    y -= 18
    total= 0
    pdf.setFont("Helvetica", 12)
    for note in notes:
        pdf.drawString(x, y, f"{note.subject} : {note.score}")
        total += note.score
        y -= 15
    if notes:
        avg= total / len(notes)
    else:
        avg= 0
    y -= 10
    pdf.drawString(x, y, f"Moyenne de l'étudiant : {round(avg,2)}")
    all_notes= Note.query.all()
    if all_notes:
        general_avg= sum(n.score for n in all_notes) / len(all_notes)
    else:
        general_avg= 0
    y -= 10
    pdf.drawString(x, y, f"Moyenne générale de la classe : {round(general_avg,2)}")
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Listing_de_notes.pdf", mimetype='application/pdf')

def general_average():
    notes= Note.query.all()
    if notes:
        total= sum(note.score for note in notes)
        avg= total / len(notes)
    else:
        avg= 0
    return round(avg, 2)

@login_required
def my_notes():
    student= Student.query.filter_by(name= student_name).first()
    if not student:
        student= Student(
            name= student_name,
            user_id= current_user.id
        )

    notes= student.notes
    return render_template('notes.html', notes= notes)