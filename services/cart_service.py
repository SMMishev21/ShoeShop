carts = {}

def add_to_cart(user_id, product_id, qty=1):

    if user_id not in carts:
        carts[user_id] = []

    for it in carts[user_id]:
        if it["product_id"] == product_id:
            it["qty"] += qty  # поправено: вече се използва 'qty', а не 'quality'
            return
    carts[user_id].append({"product_id": product_id, "qty": qty})

def get_cart(user_id):
    return carts.get(user_id, [])

def clear_cart(user_id):
    carts[user_id] = []
