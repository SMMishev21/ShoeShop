from flask import Blueprint, render_template, request
from flask import flash, redirect, url_for, session
from services import auth_service
auth_bp = Blueprint("auth", __name__)



class AuthController:

    def register(self, form_data):

        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        if not email or not password:
            flash("Попълнете всички полета.", "error")
            return redirect(url_for("auth.register"))

        user = auth_service.register_user(email, password)
        if user is None:
            flash("Потребител с този имейл вече съществува.", "error")
            return redirect(url_for("auth.register"))

        flash("Регистрацията е успешна", "success")
        return redirect(url_for("auth.login"))

    def login(self, form_data):

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

        session.pop("user_id", None)
        session.pop("is_admin", None)
        flash("Излязохте.", "info")
        return redirect(url_for("auth.login"))



class ExtendedAuthController(AuthController):

    def login(self, form_data):
        from flask import flash
        result = super().login(form_data)
        flash("Добре дошли обратно!", "info")
        return result


auth_controller = AuthController()


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
