from flask import Blueprint, render_template, request
from services import catalog_service

catalog_bp = Blueprint("catalog", __name__)

def sort_products(products, sort_by):

    if sort_by == "price_asc":
        return sorted(products, key=lambda p: p["price"])
    elif sort_by == "price_desc":
        return sorted(products, key=lambda p: p["price"], reverse=True)
    elif sort_by == "stock":
        return sorted(products, key=lambda p: p["stock"], reverse=True)
    else:
        return sorted(products, key=lambda p: p["name"].lower())


@catalog_bp.route("/catalog")
def catalog():

    q = request.args.get("q", "").strip()
    color = request.args.get("color", "").strip()
    size = request.args.get("size", "").strip()
    price_min = request.args.get("price_min", "").strip()
    price_max = request.args.get("price_max", "").strip()
    in_stock = request.args.get("in_stock", "")
    sort_by = request.args.get("sort_by", "name")

    products = catalog_service.get_all_products()


    if q:
        products = catalog_service.search_products(q)


    products = catalog_service.filter_products(
        products,
        price_min=float(price_min) if price_min else None,
        price_max=float(price_max) if price_max else None,
        size=int(size) if size else None,
        in_stock=(in_stock == "on") if in_stock else None,
        color=color if color else None
    )


    products = sort_products(products, sort_by)

    return render_template("catalog.html", products=products)
