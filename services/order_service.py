from models import Order, OrderItem, Product
from database import db


def create_order(user_id, items, address, payment):
    """Create a new order"""
    # Validate stock availability
    for item in items:
        product = Product.query.get(item["product_id"])
        if not product or product.stock < item["qty"]:
            raise Exception(f"Няма достатъчно наличност за продукт {item['product_id']}")

    # Create order
    new_order = Order(
        user_id=user_id,
        address=address,
        payment=payment,
        status='new'
    )

    db.session.add(new_order)
    db.session.flush()  # Get order ID before adding items

    # Add order items and update stock
    for item in items:
        product = Product.query.get(item["product_id"])

        # Create order item
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item["product_id"],
            qty=item["qty"],
            price=product.price  # Store current price
        )
        db.session.add(order_item)

        # Update product stock
        product.stock -= item["qty"]

    db.session.commit()

    print(f"[ORDER] Нова поръчка от user {user_id}")
    return new_order.to_dict()


def get_orders_by_user(user_id):
    """Get all orders for a specific user"""
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return [order.to_dict() for order in orders]


def get_order_by_id(order_id):
    """Get a specific order by ID"""
    order = Order.query.get(order_id)
    return order.to_dict() if order else None


def get_all_orders():
    """Get all orders (admin function)"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return [order.to_dict() for order in orders]


def update_order_status(order_id, status):
    """Update order status"""
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
        return order.to_dict()
    return None