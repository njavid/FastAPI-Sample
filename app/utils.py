from .database import SessionLocal, engine
from .models import *

def create_sample_data():
    db: Session = SessionLocal()

    # Create sample users
    user1 = db.query(User).filter(User.email == "user1@example.com").first()

    # user1 = User(email="user1@example.com", hashed_password="hashedpassword1")

    # db.add(user1)
    # db.commit()

    # Create sample products
    product1 = Product(id=1,name="Product 1", price=100)
    product2 = Product(id=2,name="Product 2", price=200)
    product3 = Product(id=3,name="Product 3", price=300)

    db.add(product1)
    db.add(product2)
    db.add(product3)
    db.commit()

    # Create sample baskets and associate products with them
    basket1 = BuyBasket(user_id=user1.id, is_active=True)
    # basket2 = BuyBasket(user_id=user2.id, is_active=True)


    db.add(basket1)
    # db.add(basket2)
    db.commit()

    # Associate products with baskets (many-to-many)
    basket1.products.append(product1)
    basket1.products.append(product2)

    db.commit()
