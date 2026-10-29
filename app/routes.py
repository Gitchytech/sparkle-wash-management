from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from database.operations import (
    add_customer,
    get_customer,
    get_customers,
    get_dashboard_summary,
    update_customer,
)

main = Blueprint("main", __name__)


@main.route("/")
def home():
    db_name = current_app.config.get("DATABASE")
    summary = get_dashboard_summary(db_name)

    return render_template("index.html", summary=summary)


@main.route("/customers", methods=["GET", "POST"])
def customers():
    db_name = current_app.config.get("DATABASE")
    error = None

    if request.method == "POST":
        name = request.form.get("name", "")

        try:
            add_customer(name, db_name)
            return redirect(url_for("main.customers"))
        except ValueError as exc:
            error = str(exc)

    customer_list = get_customers(db_name)

    return render_template(
        "customers.html",
        customers=customer_list,
        error=error,
    )


@main.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    db_name = current_app.config.get("DATABASE")
    customer = get_customer(customer_id, db_name)

    if customer is None:
        return "Customer not found", 404

    error = None

    if request.method == "POST":
        name = request.form.get("name", "")

        try:
            updated = update_customer(customer_id, name, db_name)

            if not updated:
                return "Customer not found", 404

            return redirect(url_for("main.customers"))
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "edit_customer.html",
        customer=customer,
        error=error,
    )
