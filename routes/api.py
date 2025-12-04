# from flask import Blueprint, request, jsonify, session
# from models.database import get_db
# from utils.decorators import login_required

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/api/save_answer', methods=['POST'])
# @login_required
# def save_answer():
#     data = request.get_json()
#     tentative_id = data.get('tentative_id')
#     question_id = data.get('question_id')
#     reponses = data.get('reponses', [])
#     temps_reponse = data.get('temps_reponse', 0)
    
#     db = get_db()
#     c = db.cursor()
    
#     try:
#         # Supprimer les anciennes réponses pour cette question
#         c.execute('DELETE FROM reponse_etudiant WHERE id_tentative = ? AND id_question = ?', 
#                  (tentative_id, question_id))
        
#         # Ajouter les nouvelles réponses
#         for reponse in reponses:
#             if isinstance(reponse, int) or (isinstance(reponse, str) and reponse.isdigit()):
#                 # Réponse par choix
#                 c.execute('INSERT INTO reponse_etudiant (id_tentative, id_question, id_choix, temps_reponse) VALUES (?, ?, ?, ?)', 
#                          (tentative_id, question_id, int(reponse), temps_reponse))
#             else:
#                 # Réponse texte (numérique)
#                 c.execute('INSERT INTO reponse_etudiant (id_tentative, id_question, texte_reponse, temps_reponse) VALUES (?, ?, ?, ?)', 
#                          (tentative_id, question_id, str(reponse), temps_reponse))
        
#         db.commit()
#         return jsonify({'success': True})
    
#     except Exception as e:
#         db.rollback()
#         return jsonify({'success': False, 'error': str(e)})
    
#     finally:
#         db.close()