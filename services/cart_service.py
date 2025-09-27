carts = {}

def add_to_cart(user_id, product_id, quality=1):
    if user_id not in carts:
        carts[user_id] = []

    for it in carts[user_id]:
        if it["product_id"] == product_id:
            it["quality"] += quality
            return
    carts[user_id].append({"product_id": product_id, "qty": quality})

def get_cart(user_id):
    return carts.get(user_id, [])

def clear_cart(user_id):
    carts[user_id] = []
