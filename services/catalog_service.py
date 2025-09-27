products = []

def _seed():
    if products:
        return
    products.append({
        "id": 1,
        "name": "Nike Air Zoom",
        "description": "Леки маратонки за бягане.",
        "color": "черен",
        "sizes": [40, 41, 42, 43],
        "price": 120.0,
        "stock": 10
    })
    products.append({
        "id": 2,
        "name": "Adidas Superstar",
        "description": "Класически модел.",
        "color": "бял",
        "sizes": [39, 40, 41, 42],
        "price": 90.0,
        "stock": 5
    })
    products.append({
        "id": 3,
        "name": "Puma Runner",
        "description": "Удобни за ежедневието.",
        "color": "син",
        "sizes": [40, 41, 42, 43, 44],
        "price": 75.0,
        "stock": 8
    })

def get_all_products():
    return products

def get_product_by_id(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

def search_products(query):
    q = query.lower()
    return [p for p in products if q in p["name"].lower() or q in p["color"].lower()]

def filter_products(product_list, price_min=None, price_max=None, size=None, in_stock=None, color=None):
    result = product_list
    if price_min is not None:
        result = [p for p in result if p["price"] >= price_min]
    if price_max is not None:
        result = [p for p in result if p["price"] <= price_max]
    if size is not None:
        result = [p for p in result if size in p["sizes"]]
    if in_stock is not None:
        if in_stock:
            result = [p for p in result if p["stock"] > 0]
        else:
            result = [p for p in result if p["stock"] == 0]
    if color:
        c = color.lower()
        result = [p for p in result if c in p["color"].lower()]
    return result

def add_product(name, description, color, sizes, price, stock):
    new = {
        "id": (products[-1]["id"] + 1) if products else 1,
        "name": name,
        "description": description,
        "color": color,
        "sizes": sizes,
        "price": price,
        "stock": stock
    }
    products.append(new)
    return new

def edit_product(product_id, data):
    p = get_product_by_id(product_id)
    if not p:
        return None
    p.update(data)
    return p

def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return True


_seed()
