from flask import Blueprint, render_template, redirect, url_for, session
from utils.decorators import admin_required
from models.database import get_db


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


@admin_bp.route('/users')
@admin_required
def list_users():
    """Liste des utilisateurs (étudiants, enseignants, etc.)"""
    # ici tu récupères les utilisateurs depuis la BDD
    # from models.database import User
    # users = User.query.all()
    return render_template('admin/users.html')


from datetime import datetime

@admin_bp.route('/gestion_users')
@admin_required
def gestion_users():
    """
    Gestion des utilisateurs.

    Context variables passed to the template:
        users (list): Liste des utilisateurs sous forme de dictionnaires.
    """
    db = get_db()
    users = db.execute('''
        SELECT u.nom, u.prenom, u.email, r.user_role AS role, u.date_creation
        FROM user u
        JOIN role r ON u.id_role = r.id
    ''').fetchall()

    users_list = []
    for row in users:
        user = dict(row)

        # ✅ Conversion de la date string -> datetime
        if user["date_creation"]:
            user["date_creation"] = datetime.strptime(
                user["date_creation"], "%Y-%m-%d %H:%M:%S"
            )

        users_list.append(user)

    return render_template('admin/gestion_users.html', users=users_list)


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