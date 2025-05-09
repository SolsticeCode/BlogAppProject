from flask import Blueprint, request, jsonify
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/resource', methods=['GET', 'POST', 'DELETE'])
def resource():
    """Handle GET, POST, and DELETE requests for mahasiswa."""
    if request.method == 'GET':
        conn = db.get_db()
        mahasiswa = conn.execute("SELECT * FROM mahasiswa")
        rows = mahasiswa.fetchall()
        result = [dict(row) for row in rows]
        return jsonify(result), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        new_item = request.json
        if not new_item or 'nama' not in new_item or 'nim' not in new_item or 'password' not in new_item:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mahasiswa (nama, nim, password) VALUES (?, ?, ?) RETURNING id",
            (new_item['nama'], new_item['nim'], new_item['password'])
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"id": new_id, "nama": new_item['nama'], "nim": new_item['nim']}), 201

    elif request.method == 'DELETE':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        item_to_delete = request.json
        if not item_to_delete or 'id' not in item_to_delete:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mahasiswa WHERE id = ? RETURNING id", (item_to_delete['id'],))
        deleted_id = cursor.fetchone()
        conn.commit()
        conn.close()

        if not deleted_id:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item deleted"})


@bp.route('/resource/<int:id>', methods=['GET', 'PUT'])
def get_or_update_mahasiswa_by_id(id):
    """Retrieve or update a specific mahasiswa by id."""
    if request.method == 'GET':
        conn = db.get_db()
        mahasiswa = conn.execute("SELECT * FROM mahasiswa WHERE id = ?", (id,))
        row = mahasiswa.fetchone()
        conn.close()

        if row is None:
            return jsonify({"error": "Mahasiswa not found"}), 404

        return jsonify(dict(row)), 200

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        updated_item = request.json
        if not updated_item or 'nama' not in updated_item or 'nim' not in updated_item or 'password' not in updated_item:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE mahasiswa SET nama = ?, nim = ?, password = ? WHERE id = ? RETURNING id",
            (updated_item['nama'], updated_item['nim'], updated_item['password'], id)
        )
        updated_id = cursor.fetchone()
        conn.commit()
        conn.close()

        if not updated_id:
            return jsonify({"error": "Mahasiswa not found"}), 404

        return jsonify({"message": "Mahasiswa updated"})


@bp.route('/post', methods=['GET', 'POST', 'DELETE'])
def post():
    """Handle GET, POST, and DELETE requests for post."""
    if request.method == 'GET':
        conn = db.get_db()
        posts = conn.execute("SELECT * FROM post")
        rows = posts.fetchall()
        result = [dict(row) for row in rows]
        return jsonify(result), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        new_post = request.json
        if not new_post or 'id_pemilik' not in new_post or 'judul' not in new_post or 'isi' not in new_post:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO post (id_pemilik, judul, isi) VALUES (?, ?, ?) RETURNING id",
            (new_post['id_pemilik'], new_post['judul'], new_post['isi'])
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"id": new_id, "id_pemilik": new_post['id_pemilik'], "judul": new_post['judul'], "isi": new_post['isi']}), 201

    elif request.method == 'DELETE':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        post_to_delete = request.json
        if not post_to_delete or 'id' not in post_to_delete:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM post WHERE id = ? RETURNING id", (post_to_delete['id'],))
        deleted_id = cursor.fetchone()
        conn.commit()
        conn.close()

        if not deleted_id:
            return jsonify({"error": "Post not found"}), 404

        return jsonify({"message": "Post deleted"})


@bp.route('/post/<int:id>', methods=['GET', 'PUT'])
def get_or_update_post_by_id(id):
    """Retrieve or update a specific post by id."""
    if request.method == 'GET':
        conn = db.get_db()
        post = conn.execute("SELECT * FROM post WHERE id = ?", (id,))
        row = post.fetchone()
        conn.close()

        if row is None:
            return jsonify({"error": "Post not found"}), 404

        return jsonify(dict(row)), 200

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        updated_post = request.json
        if not updated_post or 'id_pemilik' not in updated_post or 'judul' not in updated_post or 'isi' not in updated_post:
            return jsonify({"error": "Invalid input"}), 400

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE post SET id_pemilik = ?, judul = ?, isi = ? WHERE id = ? RETURNING id",
            (updated_post['id_pemilik'], updated_post['judul'], updated_post['isi'], id)
        )
        updated_id = cursor.fetchone()
        conn.commit()
        conn.close()

        if not updated_id:
            return jsonify({"error": "Post not found"}), 404

        return jsonify({"message": "Post updated"})
