import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        password = request.form['password']
        db = get_db()
        error = None

        if not nama:
            error = 'Masukkan Nama.'
        elif not nim:
            error = 'Masukkan NIM.'
        elif not password:
            error = 'Masukkan Password.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO mahasiswa (nama, nim, password) VALUES (?, ?, ?)",
                    (nama, nim, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Sudah ada akun dengan nama {nama}."
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        db = get_db()
        error = None
        mahasiswa = db.execute(
            'SELECT * FROM mahasiswa WHERE nim = ?', (nim,)
        ).fetchone()

        if mahasiswa is None:
            error = 'Masukkan nim salah.'
        elif not check_password_hash(mahasiswa['password'], password):
            error = 'Password salah.'

        if error is None:
            session.clear()
            session['user_id'] = mahasiswa['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM mahasiswa WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view