from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import promotion_service, catalog_service
from datetime import datetime

promotion_bp = Blueprint("promotion", __name__)


def _is_admin():
    return session.get("is_admin", False)


@promotion_bp.route("/promotions")
def promotions_calendar():
    """Show promotional calendar"""
    active_promotions = promotion_service.get_active_promotions()
    upcoming_promotions = promotion_service.get_upcoming_promotions()

    return render_template(
        "promotions_calendar.html",
        active_promotions=active_promotions,
        upcoming_promotions=upcoming_promotions
    )


@promotion_bp.route("/admin/promotions")
def admin_promotions():
    """Admin - manage promotions"""
    if not _is_admin():
        flash("Нямате достъп до админ панела.", "error")
        return redirect(url_for("auth.login"))

    from datetime import datetime
    all_promotions = promotion_service.get_all_promotions()
    return render_template("admin_promotions.html",
                           promotions=all_promotions,
                           current_time=datetime.now())


@promotion_bp.route("/admin/promotions/add", methods=["GET", "POST"])
def add_promotion():
    """Admin - add new promotion"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        start_date_str = request.form.get("start_date", "").strip()
        end_date_str = request.form.get("end_date", "").strip()
        discount_percent = float(request.form.get("discount_percent", 0))
        promo_code = request.form.get("promo_code", "").strip().upper()
        product_ids = request.form.getlist("product_ids")

        # Convert date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Невалиден формат на датата.", "error")
            return redirect(url_for("promotion.add_promotion"))

        if start_date >= end_date:
            flash("Началната дата трябва да е преди крайната дата.", "error")
            return redirect(url_for("promotion.add_promotion"))

        # Convert product IDs to integers
        product_ids = [int(pid) for pid in product_ids if pid]

        promotion = promotion_service.create_promotion(
            title, description, start_date, end_date,
            discount_percent, promo_code, product_ids
        )

        if promotion:
            flash("Промоцията е създадена успешно.", "success")
            return redirect(url_for("promotion.admin_promotions"))
        else:
            flash("Промо кодът вече съществува.", "error")

    # GET request - show form
    products = catalog_service.get_all_products()
    return render_template("admin_add_promotion.html", products=products)


@promotion_bp.route("/admin/promotions/edit/<int:promotion_id>", methods=["GET", "POST"])
def edit_promotion(promotion_id):
    """Admin - edit promotion"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    promotion = promotion_service.get_promotion_by_id(promotion_id)
    if not promotion:
        flash("Промоцията не е намерена.", "error")
        return redirect(url_for("promotion.admin_promotions"))

    if request.method == "POST":
        title = request.form.get("title", promotion["title"]).strip()
        description = request.form.get("description", promotion["description"]).strip()
        start_date_str = request.form.get("start_date", "").strip()
        end_date_str = request.form.get("end_date", "").strip()
        discount_percent = float(request.form.get("discount_percent", promotion["discount_percent"]))
        is_active = request.form.get("is_active") == "on"
        product_ids = request.form.getlist("product_ids")

        # Prepare update data
        update_data = {
            "title": title,
            "description": description,
            "discount_percent": discount_percent,
            "is_active": is_active,
            "product_ids": [int(pid) for pid in product_ids if pid]
        }

        # Update dates if provided
        if start_date_str:
            try:
                update_data["start_date"] = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Невалиден формат на началната дата.", "error")
                return redirect(url_for("promotion.edit_promotion", promotion_id=promotion_id))

        if end_date_str:
            try:
                update_data["end_date"] = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Невалиден формат на крайната дата.", "error")
                return redirect(url_for("promotion.edit_promotion", promotion_id=promotion_id))

        updated_promotion = promotion_service.update_promotion(promotion_id, update_data)
        if updated_promotion:
            flash("Промоцията е обновена успешно.", "success")
        else:
            flash("Грешка при обновяване на промоцията.", "error")

        return redirect(url_for("promotion.admin_promotions"))

    # GET request - show form
    products = catalog_service.get_all_products()
    return render_template("admin_edit_promotion.html", promotion=promotion, products=products)


@promotion_bp.route("/admin/promotions/delete/<int:promotion_id>")
def delete_promotion(promotion_id):
    """Admin - delete promotion"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    success = promotion_service.delete_promotion(promotion_id)
    if success:
        flash("Промоцията е изтрита успешно.", "success")
    else:
        flash("Промоцията не е намерена.", "error")

    return redirect(url_for("promotion.admin_promotions"))