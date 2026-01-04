from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from utils.decorators import admin_required
from models.database import get_db
from datetime import datetime
from werkzeug.security import generate_password_hash


admin_bp = Blueprint('admin', __name__)

def row_to_dict(row):
    """Convertit un objet Row en dictionnaire"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}



@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Tableau de bord administrateur"""
    return render_template('admin/admin.html')


@admin_bp.route('/gestion_users')
@admin_required
def gestion_users():
    """
    Gestion des utilisateurs.
    """
    db = get_db()
    users = db.execute('''
        SELECT 
            u.id,
            u.nom, 
            u.prenom, 
            u.email, 
            r.user_role AS role, 
            u.date_creation
        FROM user u
        JOIN role r ON u.id_role = r.id
    ''').fetchall()

    users_list = []
    for row in users:
        user = dict(row)

        # ✅ Conversion de la date pour que strftime fonctionne dans le template
    if user["date_creation"]:
        try:
        # Cas avec microsecondes
            user["date_creation"] = datetime.strptime(user["date_creation"], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
        # Cas sans microsecondes
            user["date_creation"] = datetime.strptime(user["date_creation"], "%Y-%m-%d %H:%M:%S")

    users_list.append(user)

    return render_template('admin/gestion_users.html', users=users_list)


@admin_bp.route('/add_user', methods=['POST'])
@admin_required  # ✅ Seul un admin peut accéder à cette route
def add_user():
    db = get_db()

    # Récupération des champs du formulaire
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    role_name = request.form.get('role')  # Rôle sélectionné
    password = request.form.get('password')

    # Vérification des champs obligatoires
    if not nom or not prenom or not email or not role_name or not password:
        flash("Tous les champs sont obligatoires.", "danger")
        return redirect(url_for('admin.gestion_users'))

    # Récupération de l'id du rôle depuis la table role
    role_row = db.execute(
        "SELECT id FROM role WHERE user_role = ?",
        (role_name,)
    ).fetchone()

    if not role_row:
        flash("Rôle invalide.", "danger")
        return redirect(url_for('admin.gestion_users'))

    role_id = role_row["id"]

    # Hashage sécurisé du mot de passe
    hashed_password = generate_password_hash(password)

    # Insertion de l'utilisateur
    db.execute(
        """
        INSERT INTO user (nom, prenom, email, password_hash, id_role, date_creation)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (nom, prenom, email, hashed_password, role_id, datetime.now())
    )

    db.commit()

    flash("Utilisateur ajouté avec succès ✅", "success")
    return redirect(url_for('admin.gestion_users'))



@admin_bp.route('/settings')
@admin_required
def settings():
    """Paramètres généraux du site"""
    return render_template('admin/settings.html')

@admin_bp.route('/reports')
@admin_required 
def reports():
    """Rapports et statistiques"""
    return render_template('admin/reports.html')
