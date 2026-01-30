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
    # 1. get data from frontend
    data = request.get_json()

    # 2. Validierung: Fehlt Titel oder Inhalt?
    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content"}), 400

    # 3. Neue ID =  (List length + 1)
    new_id = len(POSTS) + 1

    # 4. Create new dict.
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    # 5. In Liste speichern
    POSTS.append(new_post)

    # 6.  Status 201
    return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # 1. Post in der Liste suchen
    post_to_delete = None
    for post in POSTS:
        if post['id'] == id:
            post_to_delete = post
            break

    # 2. Error Handling: In case the Post doesnt exist
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # 3. Den Post aus der Liste entfernen
    POSTS.remove(post_to_delete)


    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
