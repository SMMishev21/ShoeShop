from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoeshop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()
        seed_data()


def seed_data():
    """Seed initial data if database is empty"""
    from models import User, Product

    # Check if data already exists
    if User.query.first() is not None:
        return

    # Create admin and test users
    admin = User(email="admin@123", password="admin123", is_admin=True)
    user1 = User(email="user1@123", password="user123", is_admin=False)
    user2 = User(email="user2@234", password="user234", is_admin=False)

    db.session.add_all([admin, user1, user2])

    # Create initial products
    products_data = [
        {
            "name": "Nike Air Zoom Pegasus",
            "description": "Леки маратонки за бягане с отлична амортизация и въздушна възглавница.",
            "color": "черен",
            "sizes": "40,41,42,43",
            "price": 120.0,
            "stock": 10,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Adidas Superstar Classic",
            "description": "Класически модел с иконичен дизайн, перфектен за всекидневна употреба.",
            "color": "бял",
            "sizes": "39,40,41,42",
            "price": 90.0,
            "stock": 5,
            "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Puma RS-X Runner",
            "description": "Удобни за ежедневието с модерен дизайн и цветна палитра.",
            "color": "син",
            "sizes": "40,41,42,43,44",
            "price": 75.0,
            "stock": 8,
            "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Converse Chuck Taylor All Star",
            "description": "Класически високи кецове с вечен дизайн и максимален комфорт.",
            "color": "червен",
            "sizes": "38,39,40,41,42",
            "price": 65.0,
            "stock": 12,
            "image_url": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "New Balance 574 Sport",
            "description": "Ретро маратонки с отлична поддръжка и стил за градска среда.",
            "color": "сив",
            "sizes": "40,41,42,43",
            "price": 95.0,
            "stock": 7,
            "image_url": "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Vans Old Skool",
            "description": "Скейтърски обувки с класическа черно-бяла комбинация.",
            "color": "черен",
            "sizes": "39,40,41,42,43",
            "price": 70.0,
            "stock": 15,
            "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Air Jordan 1 Retro High",
            "description": "Легендарни баскетболни обувки с култов статус и стил.",
            "color": "червен",
            "sizes": "41,42,43,44",
            "price": 180.0,
            "stock": 4,
            "image_url": "https://images.unsplash.com/photo-1556906781-9a412961c28c?auto=format&fit=crop&w=400&q=80"
        },
        {
            "name": "Reebok Club C 85 Vintage",
            "description": "Минималистични бели маратонки с винтидж излъчване.",
            "color": "бял",
            "sizes": "38,39,40,41,42",
            "price": 85.0,
            "stock": 9,
            "image_url": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?auto=format&fit=crop&w=400&q=80"
        }
    ]

    for pd in products_data:
        product = Product(**pd)
        db.session.add(product)

    db.session.commit()
    print("Database seeded successfully!")