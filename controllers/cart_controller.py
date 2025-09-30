from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from services import cart_service, catalog_service, order_service

cart_bp = Blueprint("cart", __name__)

def _current_user_id():
    return session.get("user_id")

def notify_cart_action(action, **kwargs):
    """
    Алгоритъм за нотификации в кошницата.
    action: str - какво действие се извършва
    kwargs: допълнителни данни, напр. продукт, количество, адрес
    """
    if action == "not_logged_in":
        return ("Трябва да сте влезли, за да продължите.", "error")
    elif action == "product_not_found":
        return ("Продуктът не е намерен.", "error")
    elif action == "insufficient_stock":
        return (f"Няма достатъчно наличност за продукт {kwargs.get('product_name', '')}.", "error")
    elif action == "added_to_cart":
        return (f"Продуктът {kwargs.get('product_name', '')} е добавен в кошницата.", "success")
    elif action == "empty_cart":
        return ("Кошницата е празна.", "error")
    elif action == "missing_checkout_info":
        return ("Попълнете адрес и начин на плащане.", "error")
    elif action == "order_success":
        return (f"Поръчката #{kwargs.get('order_id')} е създадена успешно.", "success")
    elif action == "sorted":
        return (f"Продуктите са сортирани по {kwargs.get('criteria')}.", "info")
    return ("Нещо се обърка.", "error")

def sort_items(items, criteria):
    """
    Алгоритъм за сортиране на продукти в кошницата.
    criteria: 'name', 'price', 'qty', 'subtotal'
    """
    if criteria == "price":
        return sorted(items, key=lambda x: x["product"]["price"])
    elif criteria == "qty":
        return sorted(items, key=lambda x: x["qty"])
    elif criteria == "subtotal":
        return sorted(items, key=lambda x: x["subtotal"])
    else:  # default: name
        return sorted(items, key=lambda x: x["product"]["name"].lower())

@cart_bp.route("/cart")
def cart():
    user_id = _current_user_id()
    items, total = [], 0
    if user_id:
        for it in cart_service.get_cart(user_id):
            p = catalog_service.get_product_by_id(it["product_id"])
            if p:
                subtotal = p["price"] * it["qty"]
                total += subtotal
                items.append({"product": p, "qty": it["qty"], "subtotal": subtotal})

    # Сортиране по критерий, подаден в GET параметър
    sort_by = request.args.get("sort_by", "name")
    items = sort_items(items, sort_by)
    if items:
        msg, category = notify_cart_action("sorted", criteria=sort_by)
        flash(msg, category)

    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user_id = _current_user_id()
    if not user_id:
        msg, category = notify_cart_action("not_logged_in")
        flash(msg, category)
        return redirect(url_for("auth.login"))

    qty = int(request.form.get("qty", 1))
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        msg, category = notify_cart_action("product_not_found")
        flash(msg, category)
        return redirect(url_for("catalog.catalog"))

    if product["stock"] < qty:
        msg, category = notify_cart_action("insufficient_stock", product_name=product["name"])
        flash(msg, category)
        return redirect(url_for("catalog.catalog"))

    cart_service.add_to_cart(user_id, product_id, qty)
    msg, category = notify_cart_action("added_to_cart", product_name=product["name"])
    flash(msg, category)
    return redirect(url_for("cart.cart"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    user_id = _current_user_id()
    if not user_id:
        msg, category = notify_cart_action("not_logged_in")
        flash(msg, category)
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        payment = request.form.get("payment", "").strip()
        if not address or not payment:
            msg, category = notify_cart_action("missing_checkout_info")
            flash(msg, category)
            return redirect(url_for("cart.checkout"))

        cart_items = cart_service.get_cart(user_id)
        if not cart_items:
            msg, category = notify_cart_action("empty_cart")
            flash(msg, category)
            return redirect(url_for("catalog.catalog"))

        order = order_service.create_order(user_id, cart_items, address, payment)
        cart_service.clear_cart(user_id)
        msg, category = notify_cart_action("order_success", order_id=order["id"])
        flash(msg, category)
        return redirect(url_for("catalog.catalog"))

    # GET -> покажи кошницата
    items, total = [], 0
    for it in cart_service.get_cart(user_id):
        p = catalog_service.get_product_by_id(it["product_id"])
        if p:
            subtotal = p["price"] * it["qty"]
            total += subtotal
            items.append({"product": p, "qty": it["qty"], "subtotal": subtotal})

    # Сортиране по GET параметър
    sort_by = request.args.get("sort_by", "name")
    items = sort_items(items, sort_by)
    if items:
        msg, category = notify_cart_action("sorted", criteria=sort_by)
        flash(msg, category)

    return render_template("checkout.html", items=items, total=total)
