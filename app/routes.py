import os
from datetime import datetime, timezone
from typing import Dict, List

from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app import app, dao, db
from app.models import Contacts, Heads, Staff, Stories, System, Trips, Users
from utils.utils import exception, get_photo_vk, stripex


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@exception
def get_system_info() -> List[System]:
    system: dao = dao.SystemDAO()
    result: List[System] = system.get_system()
    if result:
        result.__dict__.update({"is_auth": current_user.is_authenticated})
    return result


def get_photo():
    system: List[System] = get_system_info()
    random_photo_list: List[Dict] = get_photo_vk(system.vk_photo_url)
    return random_photo_list


@app.route("/get_photo")
def photo():
    try:
        return get_photo(), 200, {"ContentType": "application/json"}
    except Exception:
        return None, 500


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
    system: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("main_head")
    head_info: List[Heads] = head_query.get_head()

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_info: List[Heads] = footer_query.get_head()

    # наша история
    our_history_query: dao = dao.StoriesDAO("our_history")
    our_history_info: List[Stories] = our_history_query.get_story()

    # наши цели
    our_mission_query: dao = dao.StoriesDAO("our_mission")
    our_mission_info: List[Stories] = our_mission_query.get_story()

    # шапка путешествий
    trips_head_query: dao = dao.StoriesDAO("trips")
    trips_head_info: List[Stories] = trips_head_query.get_story()

    # сами путешествия списком
    trips_query: dao = dao.TripsDAO()
    trips_info: List[Trips] = trips_query.get_showed_trips(6)

    # шапка сотрудников
    staff_head_query: dao = dao.StoriesDAO("staff")
    staff_head_info: List[Stories] = staff_head_query.get_story()

    # сотрудники списком
    staffs_query: dao = dao.StaffDAO()
    staffs_info: List[Staff] = staffs_query.get_staff()

    # url
    url = url_for("index", _external=True)

    return render_template(
        "index.tmpl",
        system=system,
        head_info=head_info,
        our_history=our_history_info,
        our_mission=our_mission_info,
        footer_info=footer_info,
        trips_head=trips_head_info,
        trips=trips_info,
        staff_head=staff_head_info,
        staffs=staffs_info,
        url=url,
    )


@exception
@login_required
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@exception
@app.route("/register", methods=["GET"])
def register():
    # pass
    user: dao = dao.UserDAO()

    if not user.get_user():
        user.create_superuser(login="admin", password="admin", about="", is_admin=True, name="")
        flash("Создан пользователь admin с паролем admin. Смените пароль!", "success")

    flash("Действие недоступно", "warning")
    return redirect(url_for("index"))


@exception
@app.route("/login", methods=["GET"])
def login():
    return make_response("login", 401)


@exception
@app.route("/login", methods=["POST"])
def post_login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))

    username: str = request.form["username"]
    password: str = request.form["pwd"]

    if not username or not password:
        return redirect(url_for("index"))

    user_dao: dao = dao.UserDAO()

    if user_dao.check_login(username, password):
        login_user(user_dao.get_by_login(username), remember=True)
        return redirect(url_for("admin"))

    flash("Ошибка авторизации", "error")
    return redirect(url_for("index"))


@exception
@app.route("/about", methods=["GET"])
def about():
    system: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("about_head")
    head_info: List[Heads] = head_query.get_head()

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_info: List[Heads] = footer_query.get_head()

    # наша история
    our_history_query: dao = dao.StoriesDAO("our_history")
    our_history_info: List[Stories] = our_history_query.get_story()

    # наши цели
    our_mission_query: dao = dao.StoriesDAO("our_mission")
    our_mission_info: List[Stories] = our_mission_query.get_story()

    # шапка сотрудников
    staff_head_query: dao = dao.StoriesDAO("staff")
    staff_head_info: List[Stories] = staff_head_query.get_story()

    # сотрудники списком
    staffs_query: dao = dao.StaffDAO()
    staffs_info: List[Staff] = staffs_query.get_staff()

    # url
    url = url_for("about", _external=True)

    return render_template(
        "about.tmpl",
        system=system,
        head_info=head_info,
        our_history=our_history_info,
        our_mission=our_mission_info,
        footer_info=footer_info,
        staff_head=staff_head_info,
        staffs=staffs_info,
        url=url,
    )


@exception
@app.route("/travels", methods=["GET"])
def travels():
    system: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("trips_head")
    head_info: List[Heads] = head_query.get_head()

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_info: List[Heads] = footer_query.get_head()

    # наша история
    our_history_query: dao = dao.StoriesDAO("our_history")
    our_history_info: List[Stories] = our_history_query.get_story()

    # шапка путешествий
    trips_head_query: dao = dao.StoriesDAO("trips")
    trips_head_info: List[Stories] = trips_head_query.get_story()

    # сами путешествия списком
    trips_query: dao = dao.TripsDAO()
    trips_info: List[Trips] = trips_query.get_showed_trips()

    # url
    url = url_for("travels", _external=True)

    return render_template(
        "travels.tmpl",
        system=system,
        head_info=head_info,
        our_history=our_history_info,
        footer_info=footer_info,
        trips_head=trips_head_info,
        trips=trips_info,
        url=url,
    )


@app.route("/travel/<int:id_travel>", methods=["GET"])
def travel(id_travel):
    system: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("trips_head")
    head_info: List[Heads] = head_query.get_head()

    # наша история
    our_history_query: dao = dao.StoriesDAO("our_history")
    our_history_info: List[Stories] = our_history_query.get_story()

    # шапка путешествий
    trips_head_query: dao = dao.StoriesDAO("trips")
    trips_head_info: List[Stories] = trips_head_query.get_story()

    # симпл путешествия
    # сами путешествия списком
    trips_query: dao = dao.TripsDAO(id_trips=id_travel)
    trips_info: List[Trips] = trips_query.get_trip()

    # url
    url = url_for("travel", id_travel=id_travel, _external=True)

    return render_template(
        "simple_travel.tmpl",
        system=system,
        head_info=head_info,
        our_history=our_history_info,
        trips_head=trips_head_info,
        trips_info=trips_info,
        url=url,
    )


@app.route("/contact", methods=["GET"])
def contact():
    system: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("contacts_head")
    head_info: List[Heads] = head_query.get_head()

    # шапка контактов
    contact_head_query: dao = dao.StoriesDAO("contacts")
    contact_head_info: List[Stories] = contact_head_query.get_story()

    # получим контакты
    contacts: dao = dao.ContactsDAO()
    contacts_data: List[Contacts] = contacts.get_contacts()

    phones: List = contacts_data.phone

    if phones:
        phones: List = contacts_data.phone.split(";")

    # url
    url = url_for("contact", _external=True)

    return render_template(
        "contacts.tmpl",
        system=system,
        head_info=head_info,
        contact_head=contact_head_info,
        contacts=contacts_data,
        phones=phones,
        url=url,
    )


@exception
@app.route("/blog", methods=["GET"])
def blog():
    # url
    url = url_for("blog", _external=True)  # noqa: F841

    return "blog"


@exception
@app.route("/blog/<int:blog_id>", methods=["GET"])
def blog_simple(id_blog):
    # url
    url = url_for("blog_simple", id_blog=id_blog, _external=True)
    return f"blog {id_blog} - url: {url}"


# Часть Админки
@exception
@app.route("/admin", methods=["GET"], strict_slashes=False)
@login_required
def admin():
    system: List[System] = get_system_info()
    return render_template("admin/index.html", system=system)


@exception
@app.route("/admin", methods=["POST"], strict_slashes=False)
@login_required
def admin_index_save():
    statistic: str = stripex(request.form.get("statistic"))

    system_query: dao = dao.SystemDAO(1)

    system_query.save_statistic(statistic)

    return redirect(url_for("admin"))


@exception
@app.route("/admin/blog", methods=["GET"], strict_slashes=False)
@login_required
def admin_blog():
    """
    Настройка страницы блога
    """
    system_info: List[System] = get_system_info()

    title = "Блог"
    return render_template("admin/blog.html", system_info=system_info, title=title)


@exception
@app.route("/admin/system", methods=["GET"], strict_slashes=False)
@login_required
def admin_system():
    system_info: List[System] = get_system_info()
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
    bg_pic: str = stripex(request.form.get("photo_card"))
    main_video: str = stripex(request.form.get("main_video"))

    sys: dao = dao.SystemDAO(id_system)

    sys.save(title=title, icon=icon, bg_pic=bg_pic, main_video=main_video)

    flash("Сохранено", "success")
    return redirect(url_for("admin_system"))


@exception
@app.route("/admin/staff", methods=["GET"], strict_slashes=False)
@login_required
def admin_staff():
    row_list: Dict[int, str] = {
        1: "Имя~80",
        2: "Описание~250",
    }

    staff: dao = dao.StaffDAO()

    staff_list: List[Staff] = staff.get_staff()

    return render_template(
        "admin/staff.html",
        models=staff_list,
        row_list=row_list,
        filter=True,
        add=True,
        adding="/admin/empl/add",
        editing="/admin/empl/",
        deleting="/admin/empl/del/",
    )


@exception
@app.route("/admin/empl/add", methods=["GET"], strict_slashes=False)
@login_required
def admin_empl_add():
    empl: Dict = {"id": 0, "name": ""}

    return render_template("admin/empl_form.html", empl=empl)


@exception
@app.route("/admin/empl/del/<int:id_empl>", methods=["GET"], strict_slashes=False)
@login_required
def admin_empl_del(id_empl):
    empl: dao = dao.StaffDAO(id_empl)

    empl.delete_empl()
    flash("Запись удалена.", "success")
    return redirect(url_for("admin_staff"))


@exception
@app.route("/admin/empl/edit/<int:id_empl>", methods=["POST"], strict_slashes=False)
@login_required
def admin_empl_edit(id_empl):
    empl: dao = dao.StaffDAO(id_empl)

    name: str = stripex(request.form.get("name"))
    description: str = stripex(request.form.get("description"))
    vk: str = stripex(request.form.get("vk"))
    instagram: str = stripex(request.form.get("instagram"))
    telegram: str = stripex(request.form.get("telegram"))
    photo_card: str = stripex(request.form.get("photo_card"))

    empl.save(name, description, vk, instagram, telegram, photo_card)

    flash("Запись сохранена.", "success")
    return redirect(url_for("admin_staff"))


@exception
@app.route("/admin/empl/<int:id_empl>", methods=["GET"], strict_slashes=False)
@login_required
def admin_empl_show(id_empl):
    staff: dao = dao.StaffDAO(id_empl)

    empl: List[Staff] = staff.get_empl()
    return render_template("admin/empl_form.html", empl=empl)


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

    travels_query: dao = dao.TripsDAO()
    trips_list: List[Trips] = travels_query.get_trips()

    return render_template(
        "admin/trips.html",
        models=trips_list,
        row_list=row_list,
        filter=True,
        add=True,
        adding="/admin/trip/add",
        editing="/admin/trip/",
        deleting="/admin/trip/del/",
    )


@exception
@app.route("/admin/trip/<int:id_trip>", methods=["GET"], strict_slashes=False)
@login_required
def admin_trip_show(id_trip):
    travels_query: dao = dao.TripsDAO(id_trip)
    trip: List[Trips] = travels_query.get_trip()

    return render_template("admin/trip_form.html", travels=trip)


@exception
@app.route("/admin/trip/del/<int:id_trip>", methods=["GET"], strict_slashes=False)
@login_required
def admin_trip_del(id_trip):
    travels_query: dao = dao.TripsDAO(id_trip)
    travels_query.delete_trip()

    flash("Запись удалена.", "success")
    return redirect(url_for("admin_trips"))


@exception
@app.route("/admin/trip/add", methods=["GET"], strict_slashes=False)
@login_required
def admin_trip_add():
    trip: Dict = {"id": 0, "name": "", "price": "0"}

    return render_template("admin/trip_form.html", travels=trip)


@exception
@app.route("/admin/trip/edit/<int:id_trip>", methods=["POST"], strict_slashes=False)
@login_required
def admin_trip_edit(id_trip):
    travels_query: dao = dao.TripsDAO(id_trip)

    name: str = stripex(request.form.get("name"))
    price: int = stripex(request.form.get("price"))
    short_desc: str = stripex(request.form.get("short_desc"))
    description: str = stripex(request.form.get("texteditor"))
    photo_card: str = stripex(request.form.get("photo_card"))
    date_start: datetime = stripex(request.form.get("date_start"))
    date_finish: datetime = stripex(request.form.get("date_finish"))

    showed: int = 1 if request.form.get("showed") else 0

    if not date_start or not date_finish:
        flash("Даты не заполнены.", "error")
        if id_trip == 0:
            return redirect(url_for("admin_trip_add"))

        return redirect(url_for("admin_trip_show", id_trip=id_trip))

    showed: bool = bool(showed)
    travels_query.save(
        name,
        price,
        short_desc,
        description,
        photo_card,
        showed,
        date_start,
        date_finish,
    )

    flash("Запись сохранена.", "success")
    return redirect(url_for("admin_trips"))


@exception
@app.route("/admin/p/main", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_main():
    """
    Настройка главной страницы
    """
    data: Dict = {}

    system_info: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("main_head")
    head_info: List[Heads] = head_query.get_head()

    data["main_title"] = head_info.title
    data["main_desc"] = head_info.description

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_info: List[Heads] = footer_query.get_head()

    data["footer_title"] = footer_info.title
    data["footer_desc"] = footer_info.description

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

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("main_head")
    head_query.save(main_title, main_desc, "main_head")

    # нижний текст на картинке
    footer_query: dao = dao.HeadsDAO("main_footer")
    footer_query.save(footer_title, footer_desc, "main_footer")

    flash("Сохранено", "success")
    return redirect(url_for("admin_page_main_save"))


@exception
@app.route("/admin/p/about", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_about():
    """
    Настройка страницы о нас
    """
    data: Dict = {}
    system_info: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("about_head")
    head_info: List[Heads] = head_query.get_head()

    data["main_title"] = head_info.title
    data["main_desc"] = head_info.description

    title = "О нас"

    return render_template(
        "admin/about_page.html", system_info=system_info, title=title, data=data
    )


@exception
@app.route("/admin/p/about", methods=["POST"], strict_slashes=False)
@login_required
def admin_page_about_save():
    """
    Сохранение настроек О нас
    """

    main_title: str = stripex(request.form.get("main_title"))
    main_desc: str = stripex(request.form.get("main_desc"))

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("about_head")
    head_query.save(main_title, main_desc, "about_head")

    flash("Сохранено", "success")
    return redirect(url_for("admin_page_about"))


@exception
@app.route("/admin/p/trips", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_trips():
    """
    Настройка страницы путешествий
    """
    data: Dict = {}
    system_info: List[System] = get_system_info()

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("trips_head")
    head_info: List[Heads] = head_query.get_head()

    data["trips_title"] = head_info.title
    data["trips_desc"] = head_info.description

    # Заголовки возьмём в истории, тк формат тот же
    trips_query: dao = dao.StoriesDAO("trips")
    trips_info: List[Stories] = trips_query.get_story()

    data["trips_bg"] = trips_info.bg_text
    data["trips_up_text"] = trips_info.up_head
    data["trips_down_text"] = trips_info.down_head

    title = "Путешествия"

    return render_template(
        "admin/trips_page.html", system_info=system_info, title=title, data=data
    )


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
    stories_query.save("", trips_bg, trips_up_text, trips_down_text, "", "trips")

    flash("Сохранено", "success")
    return redirect(url_for("admin_page_trips"))


@exception
@app.route("/admin/p/blog", methods=["GET"], strict_slashes=False)
@login_required
def admin_page_blog():
    """
    Настройка страницы блога
    """
    system_info: List[System] = get_system_info()

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

    system_info: List[System] = get_system_info()

    # верхний текст на картинке
    contacts_query: dao = dao.HeadsDAO("contacts_head")
    contacts_info: List[Heads] = contacts_query.get_head()

    data["contacts_title"] = contacts_info.title
    data["contacts_desc"] = contacts_info.description

    # оформление
    contacts_story_query: dao = dao.StoriesDAO("contacts")
    contacts_story: List[Stories] = contacts_story_query.get_story()

    data["contacts_bg"] = contacts_story.bg_text
    data["contacts_up_text"] = contacts_story.up_head
    data["contacts_down_text"] = contacts_story.down_head

    # контакты
    contacts: dao = dao.ContactsDAO()
    contacts_list: List[Contacts] = contacts.get_contacts()

    data["vk"] = contacts_list.vk
    data["instagram"] = contacts_list.instagram
    data["telegram"] = contacts_list.telegram
    data["whatsapp"] = contacts_list.whatsapp
    data["email"] = contacts_list.email
    data["phone"] = contacts_list.phone
    data["desc"] = contacts_list.desc

    title = "Контакты"
    return render_template(
        "admin/contacts_page.html", system_info=system_info, title=title, data=data
    )


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
    whatsapp: str = stripex(request.form.get("whatsapp"))
    email: str = stripex(request.form.get("email"))
    phone: str = stripex(request.form.get("phone"))
    desc: str = stripex(request.form.get("desc"))

    contacts_bg: str = stripex(request.form.get("contacts_bg"))
    contacts_up_text: str = stripex(request.form.get("contacts_up_text"))
    contacts_down_text: str = stripex(request.form.get("contacts_down_text"))

    # верхний текст на картинке
    head_query: dao = dao.HeadsDAO("contacts_head")
    head_query.save(contacts_title, contacts_desc, "contacts_head")

    # контакты
    contacts: dao = dao.ContactsDAO()
    contacts.save(vk, instagram, telegram, whatsapp, email, phone, desc)

    # оформление
    contacts_story: dao = dao.StoriesDAO("contacts")
    contacts_story.save(
        "", contacts_bg, contacts_up_text, contacts_down_text, "", "contacts"
    )

    flash("Сохранено", "success")
    return redirect(url_for("admin_page_contacts"))


@exception
@app.route("/admin/story/<name>", methods=["GET"], strict_slashes=False)
@login_required
def admin_story(name):
    """
    Настройка страниц историй "наша история", "наша цель"
    """

    system_info: List[System] = get_system_info()

    # верхний текст на картинке
    story_query: dao = dao.StoriesDAO(name)
    story_info: List[Stories] = story_query.get_story()

    if not story_info.type_stories:
        story_info.type_stories = name

    return render_template(
        "admin/story.html", system_info=system_info, story_info=story_info
    )


@exception
@app.route("/admin/story/<name>", methods=["POST"], strict_slashes=False)
@login_required
def admin_story_save(name):
    """
    Сохранение историй
    """

    bg_text: str = stripex(request.form.get("bg_text"))
    up_head: str = stripex(request.form.get("up_head"))
    down_head: str = stripex(request.form.get("down_head"))
    text: str = stripex(request.form.get("text"))
    photo_card: str = stripex(request.form.get("photo_card"))

    story_query: dao = dao.StoriesDAO(name)
    story_query.save(
        text=text,
        bg_text=bg_text,
        up_head=up_head,
        down_head=down_head,
        pic=photo_card,
        type_stories=name,
    )

    flash("Сохранено", "success")
    return redirect(url_for("admin_story", name=name))


@exception
@app.route("/admin/user/add", methods=["GET"], strict_slashes=False)
@login_required
def admin_user_add():
    user: Dict = {"id": 0, "name": ""}

    return render_template("admin/user_form.html", data=user)


@exception
@app.route("/admin/user/del/<int:id_user>", methods=["GET"], strict_slashes=False)
@login_required
def admin_user_del(id_user):
    user: dao = dao.UserDAO(id_user)

    user.delete_user()
    flash("Запись удалена.", "success")
    return redirect(url_for("admin_users"))


@exception
@app.route("/admin/user/edit/<int:id_user>", methods=["POST"], strict_slashes=False)
@login_required
def admin_user_edit(id_user):
    login_this_user: str = stripex(request.form.get("login"))
    name: str = stripex(request.form.get("name"))
    about_user: str = stripex(request.form.get("about"))
    pwd: str = stripex(request.form.get("pwd"))
    confirm_pwd: str = stripex(request.form.get("confirm_pwd"))
    admin_flag: str = stripex(request.form.get("confirm_pwd"))

    is_admin: bool = admin_flag == "on"

    error = False

    user_query: dao = dao.UserDAO(id_user)
    user: List[Users] = user_query.get_user()
    exist_user = bool(user.id)

    if (not pwd or pwd != confirm_pwd) and not exist_user:
        flash("Пароли не совпадают", "warning")
        error = True

    if not exist_user:
        user_for_name: Users = user_query.get_by_login(login_this_user)
        if user_for_name:
            flash("Логин занят", "warning")
            error = True

    if error:
        user_data: Dict = {
            "id": user.id or 0,
            "name": name,
            "login": login,
            "about": about_user,
        }
        return render_template("admin/user_form.html", data=user_data)

    if exist_user:
        password = pwd if pwd and (pwd == confirm_pwd) else None
        user_query.create_superuser(
            login_this_user, name, password, about_user, is_admin
        )
    else:
        # создаём пользюка
        user_query.create_superuser(login_this_user, name, pwd, about_user, is_admin)

    flash("Запись сохранена.", "success")
    return redirect(url_for("admin_users"))


@exception
@app.route("/admin/user/<int:id_user>", methods=["GET"], strict_slashes=False)
@login_required
def admin_user_show(id_user):
    user_query: dao = dao.UserDAO(id_user)

    user: List[Users] = user_query.get_user()
    return render_template("admin/user_form.html", data=user)


@exception
@app.route("/admin/users", methods=["GET"], strict_slashes=False)
@login_required
def admin_users():
    row_list: Dict[int, str] = {
        2: "Имя~100",
        1: "Логин~100",
    }

    users_query: dao = dao.UserDAO()

    users_list: List[Users] = users_query.get_users()

    return render_template(
        "admin/users.html",
        models=users_list,
        row_list=row_list,
        filter=True,
        add=True,
        adding="/admin/user/add",
        editing="/admin/user/",
        deleting="/admin/user/del/",
    )


@exception
@app.route("/admin_save_vk", methods=["POST"], strict_slashes=False)
@login_required
def admin_save_vk():
    url: str = stripex(request.form.get("vk_photo_url"))

    if url:
        system: dao = dao.SystemDAO(1)
        system.save_vk_photo_link(url)
    return redirect(url_for("admin"))
