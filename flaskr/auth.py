import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a Blueprint named 'auth'
# __name__ informs in which file the blueprint is defined
# all the URLs associated with this blueprint will use
bp = Blueprint('auth', __name__, url_prefix='/auth')


# associate the URL with the function using the blueprint
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSER INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))

        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)

        return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests
            # The data is stored in a cookie that is sent to the browser
            # Browser sends it back with subsequent requests
            # Flask securely signs the data so it can’t be tampered
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# registers a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    '''
    checks if a user id is stored in the session
    gets that user’s data from the database
    stores it in g.user
    '''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    '''
    Returns a new view function that wraps the original view it’s applied to.
    Checks if a user is loaded and redirects to the login page otherwise.
    If a user is loaded the original view is called and continues normally.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
