from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from services import auth_service, user_service, order_service, pdf_service

profile_bp = Blueprint("profile", __name__)


def _current_user_id():
    return session.get("user_id")


@profile_bp.route("/profile")
def profile():
    """User profile page"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    user = auth_service.get_user_by_id(user_id)
    orders = order_service.get_orders_by_user(user_id)

    # Convert orders to dictionaries with proper items
    orders_data = []
    for order in orders:
        order_dict = order.copy()  # Create a copy of the order dict
        # Ensure items is a list, not a method
        if 'items' in order_dict and callable(order_dict['items']):
            # If items is callable (method), get the actual items
            from models import Order
            order_obj = Order.query.get(order['id'])
            if order_obj:
                order_dict['items'] = [item.to_dict() for item in order_obj.items]
        orders_data.append(order_dict)

    return render_template("profile.html", user=user, orders=orders_data)


@profile_bp.route("/profile/change_password", methods=["POST"])
def change_password():
    """Change user password"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    old_password = request.form.get("old_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    # Verify old password
    user = auth_service.get_user_by_id(user_id)
    if user['password'] != old_password:
        flash("Старата парола е грешна.", "error")
        return redirect(url_for("profile.profile"))

    # Verify new passwords match
    if new_password != confirm_password:
        flash("Новите пароли не съвпадат.", "error")
        return redirect(url_for("profile.profile"))

    if len(new_password) < 6:
        flash("Паролата трябва да е поне 6 символа.", "error")
        return redirect(url_for("profile.profile"))

    # Update password
    user_service.update_password(user_id, new_password)
    flash("Паролата е променена успешно.", "success")

    return redirect(url_for("profile.profile"))


@profile_bp.route("/profile/upload_image", methods=["POST"])
def upload_image():
    """Upload profile image"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    if 'profile_image' not in request.files:
        flash("Не е избран файл.", "error")
        return redirect(url_for("profile.profile"))

    file = request.files['profile_image']
    if file.filename == '':
        flash("Не е избран файл.", "error")
        return redirect(url_for("profile.profile"))

    result = user_service.upload_profile_image(user_id, file)
    if result:
        flash("Профилната снимка е качена и чака одобрение от администратор.", "info")
    else:
        flash("Грешка при качване на снимката. Позволени са само PNG, JPG, JPEG, GIF.", "error")

    return redirect(url_for("profile.profile"))


@profile_bp.route("/order/<int:order_id>/pdf")
def download_order_pdf(order_id):
    """Download order as PDF"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    order = order_service.get_order_by_id(order_id)
    if not order:
        flash("Поръчката не е намерена.", "error")
        return redirect(url_for("profile.profile"))

    # Verify order belongs to user (or user is admin)
    user = auth_service.get_user_by_id(user_id)
    if order['user_id'] != user_id and not user.get('is_admin'):
        flash("Нямате достъп до тази поръчка.", "error")
        return redirect(url_for("profile.profile"))

    # Generate PDF
    pdf_buffer = pdf_service.create_order_pdf(order, user)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'order_{order_id}.pdf'
    )