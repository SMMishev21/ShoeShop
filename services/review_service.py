from models import Review, Product
from database import db


def add_review(product_id, user_id, rating, comment):
    """Add a review for a product"""
    # Check if user already reviewed this product
    existing = Review.query.filter_by(
        product_id=product_id,
        user_id=user_id
    ).first()

    if existing:
        # Update existing review
        existing.rating = rating
        existing.comment = comment
    else:
        # Create new review
        new_review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            comment=comment
        )
        db.session.add(new_review)

    db.session.commit()
    return True


def get_product_reviews(product_id):
    """Get all reviews for a product"""
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return [r.to_dict() for r in reviews]


def get_product_rating_stats(product_id):
    """Get rating statistics for a product"""
    reviews = Review.query.filter_by(product_id=product_id).all()

    if not reviews:
        return {
            "average": 0,
            "count": 0,
            "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        }

    total = sum(r.rating for r in reviews)
    count = len(reviews)

    distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews:
        distribution[r.rating] += 1

    return {
        "average": round(total / count, 1),
        "count": count,
        "distribution": distribution
    }


def delete_review(review_id):
    """Delete a review (admin function)"""
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False


from models import Review, ReviewReply, Product, User
from database import db


# Add these new functions to your existing review_service.py

def add_reply(review_id, user_id, comment):
    """Add a reply to a review"""
    reply = ReviewReply(
        review_id=review_id,
        user_id=user_id,
        comment=comment
    )

    db.session.add(reply)
    db.session.commit()
    return reply.to_dict()


def get_review_by_id(review_id):
    """Get a specific review by ID"""
    review = Review.query.get(review_id)
    return review.to_dict() if review else None


def get_reply_by_id(reply_id):
    """Get a specific reply by ID"""
    reply = ReviewReply.query.get(reply_id)
    if reply:
        reply_dict = reply.to_dict()
        reply_dict['review'] = get_review_by_id(reply.review_id)
        return reply_dict
    return None


def delete_reply(reply_id):
    """Delete a reply"""
    reply = ReviewReply.query.get(reply_id)
    if reply:
        db.session.delete(reply)
        db.session.commit()
        return True
    return False


# Update the existing get_product_reviews function to include replies
def get_product_reviews(product_id):
    """Get all reviews for a product with their replies"""
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return [r.to_dict() for r in reviews]