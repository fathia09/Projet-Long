from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/connexion')
def connexion():
    return render_template('connexion.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/etudiant')
def etudiant():
    return render_template('interface_etudiant.html')

@app.route('/resultat_etudiant')
def resultat_etudiant():
    return render_template('resultats_etu.html')

@app.route('/examen-etudiant')
def examen_etudiant():
    return render_template('examen_etudiant.html')

@app.route('/enseignant')
def enseignant():
    return render_template('examen-enseignant.html')

@app.route('/profile-etudiant')
def profile_etudiant():
    return render_template('profil_etu.html')

@app.route('/classe')
def classe():
    return render_template('Classe.html')

@app.route('/statistique')
def statistique():
    return render_template('Statistique.html')


if __name__ == '__main__':
    app.run(debug=True)