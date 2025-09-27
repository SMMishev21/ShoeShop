from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from services import cart_service, catalog_service, order_service, auth_service

cart_bp = Blueprint("cart", __name__)

def _current_user_id():
    return session.get("user_id")

@cart_bp.route("/cart")
def cart():
    user_id = _current_user_id()
    items = []
    total = 0
    if user_id:
        cart_items = cart_service.get_cart(user_id)
        for it in cart_items:
            p = catalog_service.get_product_by_id(it["product_id"])
            if p:
                subtotal = p["price"] * it["qty"]
                total += subtotal
                items.append({"product": p, "qty": it["qty"], "subtotal": subtotal})
    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли, за да добавяте в кошницата.", "error")
        return redirect(url_for("auth.login"))

    qty = int(request.form.get("qty", 1))
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash("Продуктът не е намерен.", "error")
        return redirect(url_for("catalog.catalog"))

    if product["stock"] < qty:
        flash("Няма достатъчно наличност.", "error")
        return redirect(url_for("catalog.catalog"))

    cart_service.add_to_cart(user_id, product_id, qty)
    flash("Добавено в кошницата.", "success")
    return redirect(url_for("cart.cart"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    user_id = _current_user_id()
    if not user_id:
        flash("Трябва да сте влезли, за да направите поръчка.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        payment = request.form.get("payment", "").strip()
        if not address or not payment:
            flash("Попълнете адрес и начин на плащане.", "error")
            return redirect(url_for("cart.checkout"))

        cart_items = cart_service.get_cart(user_id)
        if not cart_items:
            flash("Кошницата е празна.", "error")
            return redirect(url_for("catalog.catalog"))

        # create order (service намалява наличност)
        order = order_service.create_order(user_id, cart_items, address, payment)
        cart_service.clear_cart(user_id)
        flash(f"Поръчката #{order['id']} е създадена успешно.", "success")
        return redirect(url_for("catalog.catalog"))

    # GET -> покажи кошницата за финализиране
    cart_items = cart_service.get_cart(user_id)
    items = []
    total = 0
    for it in cart_items:
        p = catalog_service.get_product_by_id(it["product_id"])
        if p:
            subtotal = p["price"] * it["qty"]
            total += subtotal
            items.append({"product": p, "qty": it["qty"], "subtotal": subtotal})
    return render_template("checkout.html", items=items, total=total)
