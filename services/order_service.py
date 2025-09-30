
from services import catalog_service

orders = []

def create_order(user_id, items, address, payment):

    for it in items:
        p = catalog_service.get_product_by_id(it["product_id"])
        if not p or p["stock"] < it["qty"]:
            raise Exception(f"Няма достатъчно наличност за продукт {it['product_id']}")

    for it in items:
        p = catalog_service.get_product_by_id(it["product_id"])
        p["stock"] -= it["qty"]

    order = {
        "id": (orders[-1]["id"] + 1) if orders else 1,
        "user_id": user_id,
        "items": items.copy(),
        "address": address,
        "payment": payment,
        "status": "new"
    }
    orders.append(order)
    print(f"[ORDER] Нова поръчка от user {user_id}")
    return order

def get_orders_by_user(user_id):
    return [o for o in orders if o["user_id"] == user_id]
