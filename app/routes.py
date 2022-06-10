from flask import (
    render_template,
    redirect,
    request,
    url_for,
    send_from_directory,
    make_response
)
from flask_login import login_user, logout_user, current_user, login_required
import os
from app import app, dao
from utils.utils import exception


@app.before_request
def before_request():
    # if current_user.is_authenticated:
    #     current_user.last_seen = datetime.utcnow()
    #     db.session.commit()
    pass


@app.route('/favicon.ico')
@exception
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@exception
@login_required
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("index"))


@exception
@app.route('/register', methods=['GET'])
def register():
    user: dao = dao.User()

    user.create_superuser(name='admin', password='admin')


@exception
@app.route('/login', methods=['GET'])
def login():
    return make_response('login', 401)


@exception
@app.route('/login', methods=['POST'])
def post_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login = request.form['username']
    password = request.form['pwd']

    if not login or not password:
        return redirect(url_for('index'))

    user_dao: dao = dao.UserDAO()

    if user_dao.check_login(login, password):
        login_user(user_dao.get_by_login(login), remember=True)

    return redirect(url_for('admin'))


@exception
@app.route('/about', methods=['GET'])
def about():
    return 'about'


@exception
@app.route('/trips', methods=['GET'])
def trips():
    return 'trips'


@app.route('/contact', methods=['GET'])
def contact():
    return 'contact'


@exception
@app.route('/blog', methods=['GET'])
def blog():
    return 'blog'


@exception
@app.route('/blog/<int:blog_id>', methods=['GET'])
def blog_simple(blog_id):
    return f'blog {blog_id}'


@exception
@app.route('/admin', methods=['GET'], strict_slashes=False)
@login_required
def admin():
    return render_template('admin/index.html')
