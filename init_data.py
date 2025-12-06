from models.database import init_db
import sqlite3
from werkzeug.security import generate_password_hash

def create_initial_data():
    """Crée des données initiales pour tester l'application"""
    db = sqlite3.connect('quiz.db')
    c = db.cursor()
     
        #Créer un admin
    password_hashAdmin = generate_password_hash('admin123')
    c.execute('''
        INSERT OR IGNORE INTO user (nom, prenom, email, password_hash, id_role) 
        VALUES ('Admin', 'Super', 'admin@test.com', ?, 
        (SELECT id FROM role WHERE user_role = 'admin'))
    ''', (password_hashAdmin,))

    #récupérer l'ID de l'admin
    c.execute("SELECT id FROM user WHERE email = 'admin@test.com'")
    result = c.fetchone()
    if result:
        admin_id = result[0]
    else:
        print("Erreur: Impossible de créer l'admin")
        db.close()
        return



    # Créer un enseignant
    password_hash = generate_password_hash('enseignant123')
    c.execute('''
        INSERT OR IGNORE INTO user (nom, prenom, email, password_hash, id_role) 
        VALUES ('Dupont', 'Pierre', 'enseignant@test.com', ?, 
        (SELECT id FROM role WHERE user_role = 'enseignant'))
    ''', (password_hash,))
    
    # Récupérer l'ID de l'enseignant
    c.execute("SELECT id FROM user WHERE email = 'enseignant@test.com'")
    result = c.fetchone()
    if result:
        enseignant_id = result[0]
    else:
        print("Erreur: Impossible de créer l'enseignant")
        db.close()
        return
    
    # Créer quelques groupes
    groupes = ['Groupe A', 'Groupe B', 'Groupe C']
    for nom_groupe in groupes:
        c.execute('INSERT OR IGNORE INTO groupe (nom, id_enseignant) VALUES (?, ?)', (nom_groupe, enseignant_id))
    
    # Créer quelques matières
    matieres = ['Mathématiques', 'Informatique', 'Physique']
    for nom_matiere in matieres:
        c.execute('INSERT OR IGNORE INTO matiere (nom, id_enseignant) VALUES (?, ?)', (nom_matiere, enseignant_id))
    
    db.commit()
    db.close()
    print("Données initiales créées avec succès!")

if __name__ == '__main__':
    init_db()
    create_initial_data()