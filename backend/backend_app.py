from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    # Query-Parameter aus der URL extrahieren
    search_title = request.args.get('title')
    search_content = request.args.get('content')
    #request.args.get(): Greift auf alles zu, was in der URL nach dem Fragezeichen
    # steht (z. B. ?title=flask).
    results = []

    # Die Liste der Posts durchsuchen
    for post in POSTS:
        # Wir prüfen, ob der Titel-Suchbegriff im Titel des Posts vorkommt
        # .lower() <--- or Case - Insensitivity. Immer lower annwenden wenn/damit die Suche nicht auf Groß-/Kleinschreibung achtet
        title_match = True
        if search_title:
            if search_title.lower() not in post['title'].lower():
                title_match = False

        # Prüfen, ob der Inhalts-Suchbegriff im Content des Posts vorkommt
        content_match = True
        if search_content:
            if search_content.lower() not in post['content'].lower():
                content_match = False

        # Wenn beides (sofern angegeben) passt, Post hinzugefügt
        if title_match and content_match:
            results.append(post)

    # Ergebnis auf "jsonisch(jasonify)" (kann auch eine leere Liste sein)
    return jsonify(results), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction')

    # Kopie von der Liste erstellen (deine gewünschte Logik)
    results = []
    for post in POSTS:
        results.append(post)

    # Error: Validierung (Deine kombinierte Logik)
    if sort_field is not None and sort_field != 'title' and sort_field != 'content':
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    # 3. Nur sortieren, wenn ein gültiges Feld da ist
    if sort_field is not None:
        direction = 'asc' # Standardwert setzen

        # Prüfung der Richtung nur, wenn sie mitgegeben wurde
        if sort_direction == 'desc':
            direction = 'desc'
        elif sort_direction == 'asc':
            direction = 'asc'
        elif sort_direction is not None:
            # User hat was getippt, aber es war weder asc noch desc
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

        # Sortier-Funktion (Anweisung für die Liste)
        def pick_field(item):
            return item[sort_field].lower()

        is_descending = False
        if direction == 'desc':
            is_descending = True

        results.sort(key=pick_field, reverse=is_descending)

    # Ergebnis auf "jsonisch(jasonify)"
    return jsonify(results)


@app.route('/api/posts', methods=['POST'])
def add_post():
    # get data from frontend
    data = request.get_json()

    # Validierung: Fehlt Titel oder Inhalt?
    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content"}), 400

    #  Neue ID =  (List length + 1)
    new_id = len(POSTS) + 1

    # Create new dict.
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    # In Liste speichern
    POSTS.append(new_post)

    # Status 201
    return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Post in der Liste suchen
    post_to_delete = None
    for post in POSTS:
        if post['id'] == id:
            post_to_delete = post
            break

    # Error Handling: In case the Post doesnt exist
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # Den Post aus der Liste entfernen
    POSTS.remove(post_to_delete)


    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # get data again
    data = request.get_json()

    # looking for post
    post_to_update = None
    for post in POSTS:
        if post['id'] == id:
            post_to_update = post
            break

    # If ID doesn't exist return (404)
    if post_to_update is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # Wenn 'title' im JSON ist, den neuen Wert nehmen, sonst alten behalten.
    if 'title' in data:
        post_to_update['title'] = data['title']

    # Wenn 'content' im JSON ist, nimm den neuen Wert, sonst behalte den alten
    if 'content' in data:
        post_to_update['content'] = data['content']

    #  Den aktualisierten Post zurückgeben (Status 200)
    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)