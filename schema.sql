
-- Création des tables du modèle

-- Table des rôles
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_role TEXT CHECK (user_role IN ('admin', 'enseignant', 'etudiant')) NOT NULL
);

-- Table des utilisateurs
CREATE TABLE user (
    id TEXT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    id_role INTEGER NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_role) REFERENCES role (id)
);

-- Table des matières
CREATE TABLE matiere (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user TEXT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user (id)
);

-- Table des quiz
CREATE TABLE quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    id_user TEXT NOT NULL,
    id_matiere INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user (id),
    FOREIGN KEY (id_matiere) REFERENCES matiere (id)
);

-- Table des questions
CREATE TABLE question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enonce TEXT NOT NULL,
    type TEXT CHECK (type IN ('QCM', 'VraiFaux', 'Texte')) NOT NULL,
    bareme FLOAT DEFAULT 1.0,
    id_quiz INTEGER NOT NULL,
    FOREIGN KEY (id_quiz) REFERENCES quiz (id)
);

-- Table des réponses
CREATE TABLE reponse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_question INTEGER NOT NULL,
    texte TEXT NOT NULL,
    est_correcte BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_question) REFERENCES question (id)
);
