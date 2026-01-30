from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_post():
    # 1. Die Daten vom Client (Frontend/Postman) holen
    data = request.get_json()

    # 2. Validierung: Fehlt Titel oder Inhalt?
    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content"}), 400

    # 3. Neue ID generieren (Länge der Liste + 1)
    new_id = len(POSTS) + 1

    # 4. Neues Dictionary erstellen
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    # 5. In die Liste speichern
    POSTS.append(new_post)

    # 6. Erfolg zurückmelden (mit Status 201)
    return jsonify(new_post), 201




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
