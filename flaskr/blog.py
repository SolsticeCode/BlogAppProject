from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, judul, isi, dibuat, id_pemilik, nama'
        ' FROM post p JOIN mahasiswa m ON p.id_pemilik = m.id'
        ' ORDER BY dibuat DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        error = None

        if not judul:
            error = 'Masukkann judul.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (judul, isi, id_pemilik)'
                ' VALUES (?, ?, ?)',
                (judul, isi, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, judul, isi, dibuat, id_pemilik, nama'
        ' FROM post p JOIN mahasiswa m ON p.id_pemilik = m.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Id post{id} tidak ada.")

    if check_author and post['id_pemilik'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        error = None

        if not judul:
            error = 'Masukkan judul.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET judul = ?, isi = ?'
                ' WHERE id = ?',
                (judul, isi, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))