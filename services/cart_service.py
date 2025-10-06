from models import CartItem
from database import db


def add_to_cart(user_id, product_id, qty=1):
    """Add product to user's cart"""
    # Check if item already exists in cart
    existing_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing_item:
        # Update quantity
        existing_item.qty += qty
    else:
        # Create new cart item
        new_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            qty=qty
        )
        db.session.add(new_item)

    db.session.commit()


def get_cart(user_id):
    """Get all cart items for a user"""
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return [item.to_dict() for item in cart_items]


def clear_cart(user_id):
    """Clear all items from user's cart"""
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def remove_from_cart(user_id, product_id):
    """Remove a specific item from cart"""
    CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).delete()
    db.session.commit()


def update_cart_quantity(user_id, product_id, qty):
    """Update quantity of a cart item"""
    cart_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if cart_item:
        if qty <= 0:
            db.session.delete(cart_item)
        else:
            cart_item.qty = qty
        db.session.commit()