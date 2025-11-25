from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from models.database import get_db
from utils.decorators import login_required, enseignant_required
from datetime import datetime
import csv
import io
import sqlite3

enseignant_bp = Blueprint('enseignant', __name__)

def row_to_dict(row):
    """Convertit un objet Row en dictionnaire"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}

@enseignant_bp.route('/dashboard')
@login_required
@enseignant_required
def dashboard():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM matiere WHERE id_enseignant = ?", (session['user_id'],))
    matieres = [row_to_dict(row) for row in c.fetchall()]
    c.execute("SELECT * FROM quiz WHERE id_enseignant = ?", (session['user_id'],))
    quiz = [row_to_dict(row) for row in c.fetchall()]
    c.execute("SELECT * FROM groupe WHERE id_enseignant = ?", (session['user_id'],))
    groupes = [row_to_dict(row) for row in c.fetchall()]
    db.close()
    return render_template('enseignant/dashboard.html', matieres=matieres, quiz=quiz, groupes=groupes)

@enseignant_bp.route('/matiere/add', methods=['POST'])
@login_required
@enseignant_required
def add_matiere():
    nom = request.form['nom']
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO matiere (nom, id_enseignant) VALUES (?, ?)", (nom, session['user_id']))
    db.commit()
    db.close()
    flash('Matière ajoutée')
    return redirect(url_for('enseignant.dashboard'))

@enseignant_bp.route('/groupe/add', methods=['POST'])
@login_required
@enseignant_required
def add_groupe():
    nom = request.form['nom']
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO groupe (nom, id_enseignant) VALUES (?, ?)", (nom, session['user_id']))
    db.commit()
    db.close()
    flash('Groupe ajouté')
    return redirect(url_for('enseignant.dashboard'))

@enseignant_bp.route('/quiz/create', methods=['GET', 'POST'])
@login_required
@enseignant_required
def create_quiz():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        duree = request.form['duree']
        id_matiere = request.form['matiere']
        groupes = request.form.getlist('groupes')
        
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO quiz (titre, description, duree, id_enseignant, id_matiere) VALUES (?, ?, ?, ?, ?)', 
                 (titre, description, duree, session['user_id'], id_matiere))
        quiz_id = c.lastrowid
        
        for groupe_id in groupes:
            c.execute('INSERT INTO quiz_groupe (id_quiz, id_groupe) VALUES (?, ?)', (quiz_id, groupe_id))
        
        db.commit()
        db.close()
        flash('Quiz créé')
        return redirect(url_for('enseignant.edit_quiz', quiz_id=quiz_id))
    
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM matiere WHERE id_enseignant = ?", (session['user_id'],))
    matieres = [row_to_dict(row) for row in c.fetchall()]
    c.execute("SELECT * FROM groupe WHERE id_enseignant = ?", (session['user_id'],))
    groupes = [row_to_dict(row) for row in c.fetchall()]
    db.close()
    return render_template('enseignant/create_quiz.html', matieres=matieres, groupes=groupes)

@enseignant_bp.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
@enseignant_required
def edit_quiz(quiz_id):
    db = get_db()
    c = db.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_question':
            enonce = request.form['enonce']
            type_q = request.form['type']
            bareme = request.form['bareme']
            duree = request.form.get('duree_question', 60)
            
            c.execute('INSERT INTO question (enonce, type, bareme, duree, id_quiz, id_enseignant) VALUES (?, ?, ?, ?, ?, ?)', 
                     (enonce, type_q, bareme, duree, quiz_id, session['user_id']))
            question_id = c.lastrowid
            
            if type_q in ['QCM_simple', 'QCM_multiple', 'Vrai_Faux']:
                choix = request.form.getlist('choix[]')
                corrects = request.form.getlist('correct[]')
                for i, choix_texte in enumerate(choix):
                    if choix_texte.strip():
                        est_correct = str(i) in corrects
                        c.execute('INSERT INTO choix_reponse (id_question, texte, est_correct) VALUES (?, ?, ?)', 
                                 (question_id, choix_texte, est_correct))
            db.commit()
            flash('Question ajoutée')
        elif action == 'publish':
            c.execute("UPDATE quiz SET status = 'publié' WHERE id = ?", (quiz_id,))
            db.commit()
            flash('Quiz publié')
    
    c.execute("SELECT * FROM quiz WHERE id = ?", (quiz_id,))
    quiz = row_to_dict(c.fetchone())
    c.execute("SELECT * FROM question WHERE id_quiz = ?", (quiz_id,))
    questions = [row_to_dict(row) for row in c.fetchall()]
    
    questions_with_choix = []
    for q in questions:
        c.execute("SELECT * FROM choix_reponse WHERE id_question = ?", (q['id'],))
        choix = [row_to_dict(row) for row in c.fetchall()]
        questions_with_choix.append({'question': q, 'choix': choix})
    
    db.close()
    return render_template('enseignant/edit_quiz.html', quiz=quiz, questions=questions_with_choix)

@enseignant_bp.route('/statistiques/<int:quiz_id>')
@login_required
@enseignant_required
def statistiques(quiz_id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM quiz WHERE id = ?", (quiz_id,))
    quiz = row_to_dict(c.fetchone())
    
    c.execute('''
        SELECT r.*, u.nom, u.prenom 
        FROM resultat_quiz r 
        JOIN user u ON r.id_etudiant = u.id 
        WHERE r.id_quiz = ? 
        ORDER BY r.score DESC
    ''', (quiz_id,))
    
    resultats = [row_to_dict(row) for row in c.fetchall()]
    scores = [r['score'] for r in resultats if r['score'] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    db.close()
    return render_template('enseignant/statistiques.html', quiz=quiz, resultats=resultats, avg_score=avg_score)

@enseignant_bp.route('/export/<int:quiz_id>')
@login_required
@enseignant_required
def export_quiz(quiz_id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM quiz WHERE id = ?", (quiz_id,))
    quiz = row_to_dict(c.fetchone())
    
    c.execute('''
        SELECT r.*, u.nom, u.prenom 
        FROM resultat_quiz r 
        JOIN user u ON r.id_etudiant = u.id 
        WHERE r.id_quiz = ? 
        ORDER BY r.score DESC
    ''', (quiz_id,))
    
    resultats = [row_to_dict(row) for row in c.fetchall()]
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Étudiant', 'Date', 'Score'])
    for r in resultats:
        writer.writerow([f"{r['prenom']} {r['nom']}", r['date_soumission'], r['score']])
    output.seek(0)
    db.close()
    
    return send_file(io.BytesIO(output.getvalue().encode()), 
                    mimetype='text/csv', 
                    as_attachment=True, 
                    download_name=f'quiz_{quiz_id}_results.csv')