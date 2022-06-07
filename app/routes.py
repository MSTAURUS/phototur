from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    send_from_directory,
)
from flask_login import login_user, logout_user, current_user, login_required
import os
from app import app
import datetime
from utils import exception


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
# <a href='https://ru.freepik.com/vectors/nature'>Nature вектор создан(а) dgim-studio - ru.freepik.com</a>

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@exception
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("index"))


@exception
@app.route('/login', methods=['GET'])
def get_login():
    return 'get login'


@exception
@app.route('/login', methods=['POST'])
def post_login():
    return 'post login'


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
