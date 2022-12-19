from typing import List

from flask import render_template

from app import app, db, models, routes


@app.errorhandler(404)
def not_found_error(error):
    system: List[models.System] = routes.get_system_info()
    return render_template("404.tmpl", system=system, head_info=[]), 404


@app.errorhandler(500)
def internal_error(error):
    system: List[models.System] = routes.get_system_info()
    db.session.rollback()
    return render_template("500.tmpl", system=system, head_info=[]), 500
