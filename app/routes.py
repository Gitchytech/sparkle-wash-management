from flask import Blueprint, current_app, render_template

from database.operations import get_dashboard_summary

main = Blueprint("main", __name__)


@main.route("/")
def home():
    db_name = current_app.config.get("DATABASE")
    summary = get_dashboard_summary(db_name)

    return render_template("index.html", summary=summary)
