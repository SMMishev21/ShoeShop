products = []


def _seed():
    if products:
        return

    # Nike Air Zoom - Black running shoes
    products.append({
        "id": 1,
        "name": "Nike Air Zoom Pegasus",
        "description": "Леки маратонки за бягане с отлична амортизация и въздушна възглавница.",
        "color": "черен",
        "sizes": [40, 41, 42, 43],
        "price": 120.0,
        "stock": 10,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=400&q=80"
    })

    # Adidas Superstar - White classic
    products.append({
        "id": 2,
        "name": "Adidas Superstar Classic",
        "description": "Класически модел с иконичен дизайн, перфектен за всекидневна употреба.",
        "color": "бял",
        "sizes": [39, 40, 41, 42],
        "price": 90.0,
        "stock": 5,
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=400&q=80"
    })

    # Puma Runner - Blue/Colorful
    products.append({
        "id": 3,
        "name": "Puma RS-X Runner",
        "description": "Удобни за ежедневието с модерен дизайн и цветна палитра.",
        "color": "син",
        "sizes": [40, 41, 42, 43, 44],
        "price": 75.0,
        "stock": 8,
        "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&w=400&q=80"
    })

    # Converse Chuck Taylor - Red
    products.append({
        "id": 4,
        "name": "Converse Chuck Taylor All Star",
        "description": "Класически високи кецове с вечен дизайн и максимален комфорт.",
        "color": "червен",
        "sizes": [38, 39, 40, 41, 42],
        "price": 65.0,
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?auto=format&fit=crop&w=400&q=80"
    })

    # New Balance 574 - Grey
    products.append({
        "id": 5,
        "name": "New Balance 574 Sport",
        "description": "Ретро маратонки с отлична поддръжка и стил за градска среда.",
        "color": "сив",
        "sizes": [40, 41, 42, 43],
        "price": 95.0,
        "stock": 7,
        "image_url": "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=400&q=80"
    })

    # Vans Old Skool - Black/White
    products.append({
        "id": 6,
        "name": "Vans Old Skool",
        "description": "Скейтърски обувки с класическа черно-бяла комбинация.",
        "color": "черен",
        "sizes": [39, 40, 41, 42, 43],
        "price": 70.0,
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=400&q=80"
    })

    # Jordan 1 - Red/Black
    products.append({
        "id": 7,
        "name": "Air Jordan 1 Retro High",
        "description": "Легендарни баскетболни обувки с култов статус и стил.",
        "color": "червен",
        "sizes": [41, 42, 43, 44],
        "price": 180.0,
        "stock": 4,
        "image_url": "https://images.unsplash.com/photo-1556906781-9a412961c28c?auto=format&fit=crop&w=400&q=80"
    })

    # Reebok Club C - White
    products.append({
        "id": 8,
        "name": "Reebok Club C 85 Vintage",
        "description": "Минималистични бели маратонки с винтидж излъчване.",
        "color": "бял",
        "sizes": [38, 39, 40, 41, 42],
        "price": 85.0,
        "stock": 9,
        "image_url": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?auto=format&fit=crop&w=400&q=80"
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


def add_product(name, description, color, sizes, price, stock, image_url=None):
    new = {
        "id": (products[-1]["id"] + 1) if products else 1,
        "name": name,
        "description": description,
        "color": color,
        "sizes": sizes,
        "price": price,
        "stock": stock,
        "image_url": image_url or "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?auto=format&fit=crop&w=400&q=80"
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