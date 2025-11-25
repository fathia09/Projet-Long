import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete_ici_changez_la'
    DATABASE = 'quiz.db'
    DEBUG = True