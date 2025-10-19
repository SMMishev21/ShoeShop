from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import catalog_service, auth_service, user_service, review_service

admin_bp = Blueprint("admin", __name__)


def _is_admin():
    return session.get("is_admin", False)


@admin_bp.route("/admin/products")
def products():
    if not _is_admin():
        flash("Нямате достъп до admin панела.", "error")
        return redirect(url_for("auth.login"))
    prods = catalog_service.get_all_products()
    return render_template("admin_products.html", products=prods)


@admin_bp.route("/admin/add_product", methods=["GET", "POST"])
def add_product():
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        color = request.form.get("color", "").strip()
        sizes_raw = request.form.get("sizes", "").strip()
        price = float(request.form.get("price", 0))
        stock = int(request.form.get("stock", 0))
        image_url = request.form.get("image_url", "").strip()

        sizes = [int(s.strip()) for s in sizes_raw.split(",") if s.strip()]

        catalog_service.add_product(name, description, color, sizes, price, stock, image_url)
        flash("Продуктът е добавен.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin_add_products.html")


@admin_bp.route("/admin/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash("Продуктът не е намерен.", "error")
        return redirect(url_for("admin.products"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name", product["name"]).strip(),
            "description": request.form.get("description", product["description"]).strip(),
            "color": request.form.get("color", product["color"]).strip(),
            "sizes": [int(s.strip()) for s in request.form.get("sizes", ",".join(map(str, product["sizes"]))).split(",")
                      if s.strip()],
            "price": float(request.form.get("price", product["price"])),
            "stock": int(request.form.get("stock", product["stock"])),
            "image_url": request.form.get("image_url", product.get("image_url"))
        }
        catalog_service.edit_product(product_id, data)
        flash("Продуктът е обновен.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin_edit_product.html", product=product)


@admin_bp.route("/admin/delete_product/<int:product_id>")
def delete_product(product_id):
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    catalog_service.delete_product(product_id)
    flash("Продуктът е изтрит.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/admin/profile_approvals")
def profile_approvals():
    """Show pending profile image approvals"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    pending_users = user_service.get_users_pending_approval()
    return render_template("admin_profile_approvals.html", users=pending_users)


@admin_bp.route("/admin/approve_image/<int:user_id>")
def approve_image(user_id):
    """Approve user profile image"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    user_service.approve_profile_image(user_id)
    flash("Профилната снимка е одобрена.", "success")
    return redirect(url_for("admin.profile_approvals"))


@admin_bp.route("/admin/reject_image/<int:user_id>")
def reject_image(user_id):
    """Reject user profile image"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    user_service.reject_profile_image(user_id)
    flash("Профилната снимка е отхвърлена.", "success")
    return redirect(url_for("admin.profile_approvals"))


@admin_bp.route("/admin/delete_review/<int:review_id>")
def delete_review(review_id):
    """Delete a review (admin only)"""
    if not _is_admin():
        flash("Нямате достъп.", "error")
        return redirect(url_for("auth.login"))

    review_service.delete_review(review_id)
    flash("Отзивът е изтрит.", "success")
    return redirect(request.referrer or url_for("admin.products"))