from models import Product
from database import db


def get_all_products():
    """Get all products from database"""
    products = Product.query.all()
    return [p.to_dict() for p in products]


def get_product_by_id(product_id):
    """Get a single product by ID"""
    product = Product.query.get(product_id)
    return product.to_dict() if product else None


def search_products(query):
    """Search products by name or color"""
    q = query.lower()
    products = Product.query.filter(
        db.or_(
            Product.name.ilike(f'%{q}%'),
            Product.color.ilike(f'%{q}%')
        )
    ).all()
    return [p.to_dict() for p in products]


def filter_products(product_list, price_min=None, price_max=None, size=None, in_stock=None, color=None):
    """Filter products based on criteria"""
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
    """Add a new product to database"""
    # Convert sizes list to comma-separated string
    sizes_str = ','.join(map(str, sizes))

    new_product = Product(
        name=name,
        description=description,
        color=color,
        sizes=sizes_str,
        price=price,
        stock=stock,
        image_url=image_url or "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?auto=format&fit=crop&w=400&q=80"
    )

    db.session.add(new_product)
    db.session.commit()

    return new_product.to_dict()


def edit_product(product_id, data):
    """Edit an existing product"""
    product = Product.query.get(product_id)
    if not product:
        return None

    # Update fields if provided
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'color' in data:
        product.color = data['color']
    if 'sizes' in data:
        # Convert list to comma-separated string
        product.sizes = ','.join(map(str, data['sizes']))
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    if 'image_url' in data:
        product.image_url = data['image_url']

    db.session.commit()
    return product.to_dict()


def delete_product(product_id):
    """Delete a product from database"""
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False