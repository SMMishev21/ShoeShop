users = []

def _seed():
    if users:
        return
    users.append({"id": 1, "email": "admin@123", "password": "admin123", "is_admin": True})
    users.append({"id": 2, "email": "user1@123", "password": "user123", "is_admin": False})
    users.append({"id": 3, "email": "user2@234", "password": "user234", "is_admin": False})

def register_user(email, password, is_admin=False):
    for u in users:
        if u["email"].lower() == email.lower():
            return None
    new_user = {
        "id": (users[-1]["id"] + 1) if users else 1,
        "email": email,
        "password": password,
        "is_admin": is_admin
    }
    users.append(new_user)
    print(f"Потвърждение за регистрацията на {email}")
    return new_user

def login_user(email, password):
    for u in users:
        if u["email"].lower() == email.lower() and u["password"] == password:
            return u
    return None

def get_user_by_id(user_id):
    for u in users:
        if u["id"] == user_id:
            return u
    return None

_seed()
