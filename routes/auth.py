from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db
from utils.decorators import login_required
import sqlite3

auth_bp = Blueprint('auth', __name__)

def row_to_dict(row):
    """Convertit un objet Row en dictionnaire"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        role_type = request.form['role']
        id_groupe = request.form.get('groupe')
        
        # Si c'est un étudiant sans groupe, on ne peut pas l'inscrire
        if role_type == 'etudiant' and not id_groupe:
            flash('Veuillez sélectionner un groupe pour les étudiants')
            return redirect(url_for('auth.register'))
        
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM role WHERE user_role = ?", (role_type,))
        role = c.fetchone()
        
        try:
            # Pour les enseignants, id_groupe est NULL
            if role_type == 'enseignant':
                c.execute("INSERT INTO user (nom, prenom, email, password_hash, id_role) VALUES (?, ?, ?, ?, ?)",
                         (nom, prenom, email, generate_password_hash(password), role[0]))
            else:
                c.execute("INSERT INTO user (nom, prenom, email, password_hash, id_role, id_groupe) VALUES (?, ?, ?, ?, ?, ?)",
                         (nom, prenom, email, generate_password_hash(password), role[0], id_groupe))
            
            db.commit()
            flash('Inscription réussie!')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email déjà utilisé')
        finally:
            db.close()
    
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM groupe")
    groupes = [row_to_dict(row) for row in c.fetchall()]
    db.close()
    
    return render_template('auth/register.html', groupes=groupes)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute('''
            SELECT u.*, r.user_role, g.nom as groupe_nom, g.id as groupe_id 
            FROM user u 
            JOIN role r ON u.id_role = r.id 
            LEFT JOIN groupe g ON u.id_groupe = g.id 
            WHERE u.email = ?
        ''', (email,))
        user_row = c.fetchone()
        db.close()
        
        if user_row:
            user = row_to_dict(user_row)
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['nom'] = user['nom']
                session['prenom'] = user['prenom']
                session['role'] = user['user_role']
                session['groupe'] = user['groupe_nom']
                session['id_groupe'] = user['groupe_id']
                return redirect(url_for('dashboard'))
        
        flash('Email ou mot de passe incorrect')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))