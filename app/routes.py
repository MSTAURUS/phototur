from flask import (
    render_template,
    redirect,
    request,
    url_for,
    send_from_directory,
    make_response,
    flash,
)
from flask_login import login_user, logout_user, current_user, login_required
import os
from app import app, dao, db
from datetime import timezone
from utils.utils import exception, stripex
from typing import Dict, List
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/favicon.ico")
@exception
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@exception
@login_required
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@exception
@app.route("/register", methods=["GET"])
def register():
    user: dao = dao.UserDAO()

    user.create_superuser(login="admin", password="admin")


@exception
@app.route("/login", methods=["GET"])
def login():
    return make_response("login", 401)


@exception
@app.route("/login", methods=["POST"])
def post_login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    username = request.form["username"]
    password = request.form["pwd"]

    if not username or not password:
        return redirect(url_for("index"))

    user_dao: dao = dao.UserDAO()

    if user_dao.check_login(username, password):
        login_user(user_dao.get_by_login(username), remember=True)

    return redirect(url_for("admin"))


@exception
@app.route("/about", methods=["GET"])
def about():
    return "about"


@exception
@app.route("/trips", methods=["GET"])
def trips():
    return "trips"


@app.route("/contact", methods=["GET"])
def contact():
    return "contact"


@exception
@app.route("/blog", methods=["GET"])
def blog():
    return "blog"


@exception
@app.route("/blog/<int:blog_id>", methods=["GET"])
def blog_simple(blog_id):
    return f"blog {blog_id}"


# Часть Админки
@exception
@app.route("/admin", methods=["GET"], strict_slashes=False)
@login_required
def admin():
    return render_template("admin/index.html")


@exception
@app.route("/admin/system", methods=["GET"], strict_slashes=False)
@login_required
def admin_system():
    system_info: dao = dao.SystemDAO.get_system()
    # print(system_info)
    # if not system_info:
    #     flash('Ошибка получения данных', 'error')
    #     return redirect(url_for("admin"))
    return render_template("admin/system.html", system_info=system_info)


@exception
@app.route("/admin/system", methods=["POST"], strict_slashes=False)
@login_required
def admin_system_save():
    id_system: int = int(stripex(request.form.get("id")) or 0)
    title: str = stripex(request.form.get("title"))
    icon: str = stripex(request.form.get("icon"))
    bg_pic: str = stripex(request.form.get("bg_pic"))
    main_video: str = stripex(request.form.get("main_video"))

    sys: dao = dao.SystemDAO(id_system)

    sys.update(title, icon, bg_pic, main_video)

    return redirect(url_for("admin_system"))


@exception
@app.route("/admin/trips", methods=["GET"], strict_slashes=False)
@login_required
def admin_trips():
    row_list: Dict[int, str] = {
        1: "Название~250",
        8: "Сезон~60",
        6: "Отображение~15",
        2: "Цена~15",
    }

    travels: dao = dao.TripsDAO(None)

    trips_list: List = travels.get_trips()

    return render_template(
        "admin/trips.html",
        models=trips_list,
        row_list=row_list,
        filter=True,
        add=True,
        adding="/admin/trip/0",
        editing="/admin/trip/",
        deleting="/admin/trip/del/",
    )


@exception
@app.route("/admin/trip/<int:id_trip>", methods=["GET"], strict_slashes=False)
@login_required
def admin_trip_show(id_trip):
    # 0 для новых
    if id_trip <= 0:
        id_trip = None

    travels: dao = dao.TripsDAO(id_trip)

    trip = travels.get_trip()
    return render_template("admin/trip_form.html", travels=trip)


@exception
@app.route("/admin/trip/del/<int:id_trip>", methods=["GET"], strict_slashes=False)
@login_required
def admin_trip_del(id_trip):
    travels: dao = dao.TripsDAO(id_trip)

    travels.delete_trip()
    flash("Запись удалена.", "success")
    return redirect(url_for("admin_trips"))


@exception
@app.route("/admin/trip/add/<int:id_trip>", methods=["POST"], strict_slashes=False)
@login_required
def admin_trip_add(id_trip):
    # 0 для новых
    if id_trip <= 0:
        id_trip = None
    travels: dao = dao.TripsDAO(id_trip)

    name: str = stripex(request.form.get("name"))
    price: int = stripex(request.form.get("price"))
    short_desc: str = stripex(request.form.get("short_desc"))
    description: str = stripex(request.form.get("description"))
    photo_list: str = stripex(request.form.get("photo_list"))
    showed: int = 0
    if request.form.get("showed"):
        showed = 1

    travels.update(name, price, short_desc, description, photo_list, showed)
    flash("Запись добавлена.", "success")
    return redirect(url_for("admin_trips"))
