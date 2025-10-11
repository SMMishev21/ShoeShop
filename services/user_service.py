from models import User
from database import db
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_password(user_id, new_password):
    """Update user password"""
    user = User.query.get(user_id)
    if user:
        user.password = new_password
        db.session.commit()
        return True
    return False


def upload_profile_image(user_id, file):
    """Upload profile image (pending admin approval)"""
    if not file or not allowed_file(file.filename):
        return None

    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Secure filename and save
    filename = secure_filename(f"user_{user_id}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Update user record
    user = User.query.get(user_id)
    if user:
        user.profile_image = f"/static/uploads/profiles/{filename}"
        user.profile_image_approved = False  # Needs admin approval
        db.session.commit()
        return user.profile_image

    return None


def approve_profile_image(user_id):
    """Approve user profile image (admin only)"""
    user = User.query.get(user_id)
    if user:
        user.profile_image_approved = True
        db.session.commit()
        return True
    return False


def reject_profile_image(user_id):
    """Reject and remove profile image (admin only)"""
    user = User.query.get(user_id)
    if user and user.profile_image:
        # Delete file if exists
        try:
            filepath = user.profile_image.lstrip('/')
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass

        user.profile_image = None
        user.profile_image_approved = False
        db.session.commit()
        return True
    return False


def get_users_pending_approval():
    """Get all users with pending profile images (admin)"""
    users = User.query.filter(
        User.profile_image.isnot(None),
        User.profile_image_approved == False
    ).all()
    return [u.to_dict() for u in users]