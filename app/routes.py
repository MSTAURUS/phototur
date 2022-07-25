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


@exception
def get_system_info() -> List:
    system: dao = dao.SystemDAO()
    return system.get_system()


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
    pass
    # user: dao = dao.UserDAO()

    # user.create_superuser(login="admin", password="admin")


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
    system_info: List = get_system_info()
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

    sys.save(title, icon, bg_pic, main_video)

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

    travels: dao = dao.TripsDAO()

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

    travels.save(name, price, short_desc, description, photo_list, showed)
    flash("Запись добавлена.", "success")
    return redirect(url_for("admin_trips"))


@exception
@app.route("/admin/p/main", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_main():
    """
    Настройка главной страницы
    """
    data: Dict = {}

    system_info: List = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("main_head")
    head_info: List = head_query.get_head()

    print(head_info)

    data["main_title"] = head_info.title
    data["main_desc"] = head_info.description

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_info: List = footer_query.get_head()

    data["footer_title"] = footer_info.title
    data["footer_desc"] = footer_info.description

    # блок наша история
    stories_query: dao = dao.StoriesDAO("our")
    story_info: List = stories_query.get_story()

    data["story_bg"] = story_info.bg_text
    data["story_up_text"] = story_info.up_head
    data["story_down_text"] = story_info.down_head
    data["story_text"] = story_info.text
    data["story_pic"] = story_info.pic

    # print(system_info)
    # if not system_info:
    #     flash('Ошибка получения данных', 'error')
    #     return redirect(url_for("admin"))

    title = "Главная страница"
    return render_template(
        "admin/main_page.html", system_info=system_info, data=data, title=title
    )


@exception
@app.route("/admin/p/main", methods=["POST"], strict_slashes=False)
@login_required
def admin_page_main_save():
    """
    Сохранение настроек главной страницы
    """

    main_title: str = stripex(request.form.get("main_title"))
    main_desc: str = stripex(request.form.get("main_desc"))
    footer_title: str = stripex(request.form.get("footer_title"))
    footer_desc: str = stripex(request.form.get("footer_desc"))
    type_head: str = stripex(request.form.get("type_head"))

    story_bg: str = stripex(request.form.get("story_bg"))
    story_up_text: str = stripex(request.form.get("story_up_text"))
    story_down_text: str = stripex(request.form.get("story_down_text"))
    story_text: str = stripex(request.form.get("story_text"))
    story_pic: str = stripex(request.form.get("story_pic"))

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("main_head")
    head_query.save(main_title, main_desc, "main_head")

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_query.save(footer_title, footer_desc, "main_footer")

    # блок наша история
    stories_query: dao = dao.StoriesDAO("our")
    stories_query.save(
        story_text, story_bg, story_up_text, story_down_text, story_pic, "our"
    )

    return redirect(url_for("admin_page_main"))


@exception
@app.route("/admin/p/about", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_about():
    """
    Настройка страницы о нас
    """
    system_info: List = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("about_head")
    head_info: List = head_query.get_head()

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("about_footer")
    footer_info: List = footer_query.get_head()

    # блок нашей команды
    staff_query: dao = dao.HeadsDAO("main_staff")
    staff_info: List = staff_query.get_head()

    # блок наша история
    stories_query: dao = dao.StoriesDAO("our")
    story_info: List = stories_query.get_story()

    # блок наша миссия
    mission_query: dao = dao.StoriesDAO("mission")
    mission_info: List = mission_query.get_story()

    # print(system_info)
    # if not system_info:
    #     flash('Ошибка получения данных', 'error')
    #     return redirect(url_for("admin"))

    title = "О нас"
    return render_template(
        "admin/about_page.html", system_info=system_info, title=title
    )


@exception
@app.route("/admin/p/trips", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_trips():
    """
    Настройка страницы путешествий
    """
    data: Dict = {}
    system_info: List = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("trips_head")
    head_info: List = head_query.get_head()

    data["trips_title"] = head_info.title
    data["trips_desc"] = head_info.description

    # Заголовки возьмём в истории, тк формат тот же
    trips_query: dao = dao.StoriesDAO("trips")
    trips_info: List = trips_query.get_story()

    data["trips_bg"] = trips_info.bg_text
    data["trips_up_text"] = trips_info.up_head
    data["trips_down_text"] = trips_info.down_head

    title = "Путешествия"

    return render_template("admin/trips_page.html", system_info=system_info, title=title, data=data)


@exception
@app.route("/admin/p/trips", methods=["POST"], strict_slashes=False)
@login_required
def admin_page_trips_save():
    """
    Сохранение настроек путешествий
    """

    trips_title: str = stripex(request.form.get("trips_title"))
    trips_desc: str = stripex(request.form.get("trips_desc"))

    trips_bg: str = stripex(request.form.get("trips_bg"))
    trips_up_text: str = stripex(request.form.get("trips_up_text"))
    trips_down_text: str = stripex(request.form.get("trips_down_text"))

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("trips_head")
    head_query.save(trips_title, trips_desc, "trips_head")

    # Сохранение заголовка
    stories_query: dao = dao.StoriesDAO("trips")
    stories_query.save('', trips_bg, trips_up_text, trips_down_text, '', "trips")

    return redirect(url_for("admin_page_trips"))


@exception
@app.route("/admin/p/blog", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_blog():
    """
    Настройка страницы блога
    """
    system_info: List = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("blog_head")
    head_info: List = head_query.get_head()

    title = "Блог"
    return render_template("admin/blog_page.html", system_info=system_info, title=title)


@exception
@app.route("/admin/p/contacts", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_contacts():
    """
    Настройка страницы contacts
    """
    data: Dict = {}

    system_info = get_system_info()

    # верхний текст на картинке
    contacts_query: dao = dao.HeadsDAO("contacts_head")
    contacts_info: List = contacts_query.get_head()

    data["contacts_title"] = contacts_info.title
    data["contacts_desc"] = contacts_info.description

    # контакты
    contacts: dao = dao.ContactsDAO()
    contacts_list: List = contacts.get_contacts()

    data["vk"] = contacts_list.vk
    data["instagram"] = contacts_list.instagram
    data["telegram"] = contacts_list.telegram
    data["email"] = contacts_list.email
    data["phone"] = contacts_list.phone
    data["desc"] = contacts_list.desc

    title = "Контакты"
    return render_template("admin/contacts_page.html", system_info=system_info, title=title, data=data)


@exception
@app.route("/admin/p/contacts", methods=["POST"], strict_slashes=False)
@login_required
def admin_page_contacts_save():
    """
    Сохранение настроек контактов
    """

    contacts_title: str = stripex(request.form.get("contacts_title"))
    contacts_desc: str = stripex(request.form.get("contacts_desc"))

    vk: str = stripex(request.form.get("vk"))
    instagram: str = stripex(request.form.get("instagram"))
    telegram: str = stripex(request.form.get("telegram"))
    email: str = stripex(request.form.get("email"))
    phone: str = stripex(request.form.get("phone"))
    desc: str = stripex(request.form.get("desc"))

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("contacts_head")
    head_query.save(contacts_title, contacts_desc, "contacts_head")

    # контакты
    contacts: dao = dao.ContactsDAO()
    contacts.save(vk, instagram, telegram, email, phone, desc)

    return redirect(url_for("admin_page_contacts"))
