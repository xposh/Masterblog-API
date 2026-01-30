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

    # Wenn 'title' im JSON ist, nimm den neuen Wert, sonst behalte den alten
    if 'title' in data:
        post_to_update['title'] = data['title']

    # Wenn 'content' im JSON ist, nimm den neuen Wert, sonst behalte den alten
    if 'content' in data:
        post_to_update['content'] = data['content']

    #  Den aktualisierten Post zurückgeben (Status 200)
    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
