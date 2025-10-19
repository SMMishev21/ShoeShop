from models import Promotion, PromotionProduct, Product
from database import db
from datetime import datetime


def get_all_promotions():
    """Get all promotions"""
    promotions = Promotion.query.order_by(Promotion.start_date.desc()).all()
    return [p.to_dict() for p in promotions]


def get_active_promotions():
    """Get currently active promotions"""
    now = datetime.now()
    promotions = Promotion.query.filter(
        Promotion.start_date <= now,
        Promotion.end_date >= now,
        Promotion.is_active == True
    ).order_by(Promotion.start_date.asc()).all()
    return [p.to_dict() for p in promotions]


def get_upcoming_promotions():
    """Get upcoming promotions (starting in the future)"""
    now = datetime.now()
    promotions = Promotion.query.filter(
        Promotion.start_date > now,
        Promotion.is_active == True
    ).order_by(Promotion.start_date.asc()).all()
    return [p.to_dict() for p in promotions]


def get_promotion_by_id(promotion_id):
    """Get promotion by ID"""
    promotion = Promotion.query.get(promotion_id)
    return promotion.to_dict() if promotion else None


def get_promotion_by_code(promo_code):
    """Get promotion by promo code"""
    promotion = Promotion.query.filter_by(promo_code=promo_code).first()
    return promotion.to_dict() if promotion else None


def create_promotion(title, description, start_date, end_date, discount_percent, promo_code, product_ids=None):
    """Create a new promotion"""
    # Check if promo code already exists
    existing = Promotion.query.filter_by(promo_code=promo_code).first()
    if existing:
        return None

    promotion = Promotion(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        discount_percent=discount_percent,
        promo_code=promo_code.upper()
    )

    db.session.add(promotion)
    db.session.flush()  # Get the promotion ID

    # Add products to promotion if provided
    if product_ids:
        for product_id in product_ids:
            product = Product.query.get(product_id)
            if product:
                promotion_product = PromotionProduct(
                    promotion_id=promotion.id,
                    product_id=product_id
                )
                db.session.add(promotion_product)

    db.session.commit()
    return promotion.to_dict()


def update_promotion(promotion_id, data):
    """Update an existing promotion"""
    promotion = Promotion.query.get(promotion_id)
    if not promotion:
        return None

    if 'title' in data:
        promotion.title = data['title']
    if 'description' in data:
        promotion.description = data['description']
    if 'start_date' in data:
        promotion.start_date = data['start_date']
    if 'end_date' in data:
        promotion.end_date = data['end_date']
    if 'discount_percent' in data:
        promotion.discount_percent = data['discount_percent']
    if 'is_active' in data:
        promotion.is_active = data['is_active']

    # Update products if provided
    if 'product_ids' in data:
        # Remove existing product associations
        PromotionProduct.query.filter_by(promotion_id=promotion_id).delete()

        # Add new product associations
        for product_id in data['product_ids']:
            product = Product.query.get(product_id)
            if product:
                promotion_product = PromotionProduct(
                    promotion_id=promotion_id,
                    product_id=product_id
                )
                db.session.add(promotion_product)

    db.session.commit()
    return promotion.to_dict()


def delete_promotion(promotion_id):
    """Delete a promotion"""
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        # Delete associated products first
        PromotionProduct.query.filter_by(promotion_id=promotion_id).delete()
        db.session.delete(promotion)
        db.session.commit()
        return True
    return False


def get_promotions_for_product(product_id):
    """Get active promotions for a specific product"""
    now = datetime.now()
    promotions = Promotion.query.join(PromotionProduct).filter(
        PromotionProduct.product_id == product_id,
        Promotion.start_date <= now,
        Promotion.end_date >= now,
        Promotion.is_active == True
    ).all()
    return [p.to_dict() for p in promotions]


def get_promotions_for_date(date):
    """Get promotions active on a specific date"""
    promotions = Promotion.query.filter(
        Promotion.start_date <= date,
        Promotion.end_date >= date,
        Promotion.is_active == True
    ).all()
    return [p.to_dict() for p in promotions]