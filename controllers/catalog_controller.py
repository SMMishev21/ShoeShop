from flask import Blueprint, render_template, request
from services import catalog_service, auth_service

catalog_bp = Blueprint("catalog", __name__)

@catalog_bp.route("/catalog")
def catalog():
    # извличане на параметрите за търсене/филтриране
    q = request.args.get("q", "").strip()
    color = request.args.get("color", "").strip()
    size = request.args.get("size", "").strip()
    price_min = request.args.get("price_min", "").strip()
    price_max = request.args.get("price_max", "").strip()
    in_stock = request.args.get("in_stock", "")  # "on" ако checked

    products = catalog_service.get_all_products()

    if q:
        products = catalog_service.search_products(q)

    # филтриране в зависимост от зададените полета
    products = catalog_service.filter_products(
        products,
        price_min=float(price_min) if price_min else None,
        price_max=float(price_max) if price_max else None,
        size=int(size) if size else None,
        in_stock=(in_stock == "on") if in_stock else None,
        color=color if color else None
    )

    return render_template("catalog.html", products=products)
