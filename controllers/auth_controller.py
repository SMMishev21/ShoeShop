from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import auth_service

auth_bp = Blueprint("auth", __name__)

class AuthController:
    """
    Клас за управление на автентикация.
    """

    def register(self, form_data):
        # Инкапсулация: цялата логика за регистрация е вътре в метода и е скрита за външния свят
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        if not email or not password:
            flash("Попълнете всички полета.", "error")
            return redirect(url_for("auth.register"))

        # Абстракция: извикваме auth_service без да показваме как точно работи той
        user = auth_service.register_user(email, password)
        if user is None:
            flash("Потребител с този имейл вече съществува.", "error")
            return redirect(url_for("auth.register"))

        flash("Регистрацията е успешна", "success")
        return redirect(url_for("auth.login"))

    def login(self, form_data):
        # Инкапсулация: цялата логика за логин е скрита вътре в метода
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        user = auth_service.login_user(email, password)
        if not user:
            flash("Грешен имейл или парола.", "error")
            return redirect(url_for("auth.login"))

        session["user_id"] = user["id"]
        session["is_admin"] = user.get("is_admin", False)
        flash("Влязохте успешно.", "success")
        return redirect(url_for("catalog.catalog"))

    def logout(self):
        # Инкапсулация: скриваме логиката за изход
        session.pop("user_id", None)
        session.pop("is_admin", None)
        flash("Излязохте.", "info")
        return redirect(url_for("auth.login"))

# Създаваме инстанс на контролера
auth_controller = AuthController()
# Полиморфизъм: можем да създадем друг клас, който наследява AuthController и презаписва методите
# без да променяме кода на Blueprint-а

# Blueprint маршрутите използват методите на класа
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return auth_controller.register(request.form)
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return auth_controller.login(request.form)
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    return auth_controller.logout()
