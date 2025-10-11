from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import catalog_service, review_service

product_bp = Blueprint("product", __name__)


def _current_user_id():
    return session.get("user_id")


@product_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    """Show product detail page with reviews"""
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash("Продуктът не е намерен.", "error")
        return redirect(url_for("catalog.catalog"))

    # Get reviews and ratings
    reviews = review_service.get_product_reviews(product_id)
    rating_stats = review_service.get_product_rating_stats(product_id)

    user_id = _current_user_id()
    user_review = None
    if user_id:
        # Check if current user already reviewed
        user_review = next((r for r in reviews if r['user_id'] == user_id), None)

    return render_template(
        "product_detail.html",
        product=product,
        reviews=reviews,
        rating_stats=rating_stats,
        user_review=user_review
    )


@product_bp.route("/product/<int:product_id>/review", methods=["POST"])
def add_review(product_id):
    """Add or update a review"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли, за да оставите отзив.", "error")
        return redirect(url_for("auth.login"))

    rating = int(request.form.get("rating", 0))
    comment = request.form.get("comment", "").strip()

    if rating < 1 or rating > 5:
        flash("Моля изберете рейтинг от 1 до 5 звезди.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    review_service.add_review(product_id, user_id, rating, comment)
    flash("Вашият отзив е добавен успешно.", "success")

    return redirect(url_for("product.product_detail", product_id=product_id))


@product_bp.route("/product/<int:product_id>/review/<int:review_id>/reply", methods=["POST"])
def add_reply(product_id, review_id):
    """Add a reply to a review"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли, за да отговорите.", "error")
        return redirect(url_for("auth.login"))

    reply_text = request.form.get("reply_text", "").strip()

    if not reply_text:
        flash("Моля въведете текст за отговора.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    review_service.add_reply(review_id, user_id, reply_text)
    flash("Вашият отговор е добавен успешно.", "success")

    return redirect(url_for("product.product_detail", product_id=product_id) + f"#review-{review_id}")


@product_bp.route("/product/<int:product_id>/review/<int:review_id>/delete", methods=["POST"])
def delete_review(product_id, review_id):
    """Delete a review"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    review = review_service.get_review_by_id(review_id)
    if not review:
        flash("Отзивът не е намерен.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    # Check if user owns the review or is admin
    if review['user_id'] != user_id and not session.get('is_admin'):
        flash("Нямате права да изтриете този отзив.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    review_service.delete_review(review_id)
    flash("Отзивът е изтрит успешно.", "success")

    return redirect(url_for("product.product_detail", product_id=product_id))


@product_bp.route("/product/<int:product_id>/reply/<int:reply_id>/delete", methods=["POST"])
def delete_reply(product_id, reply_id):
    """Delete a reply"""
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли.", "error")
        return redirect(url_for("auth.login"))

    reply = review_service.get_reply_by_id(reply_id)
    if not reply:
        flash("Отговорът не е намерен.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    # Check if user owns the reply or is admin
    if reply['user_id'] != user_id and not session.get('is_admin'):
        flash("Нямате права да изтриете този отговор.", "error")
        return redirect(url_for("product.product_detail", product_id=product_id))

    review_service.delete_reply(reply_id)
    flash("Отговорът е изтрит успешно.", "success")

    return redirect(url_for("product.product_detail", product_id=product_id))