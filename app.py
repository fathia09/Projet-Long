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


if __name__ == '__main__':
    app.run(debug=True)