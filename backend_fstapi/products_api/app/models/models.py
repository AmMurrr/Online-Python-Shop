from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # New column for role
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")

    carts = relationship("Cart", back_populates="user")

    sale = relationship("Sales", back_populates="user")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="carts")

    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationship with cart and product
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # Relationship with category
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")


    cart_items = relationship("CartItem", back_populates="product")

    sale_detail = relationship("Sales_details", back_populates="product")


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    sale_date = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_cost = Column(Float, nullable=False)

    # Relationship with user
    user_id = Column(Integer, ForeignKey("users.id",ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="sale")

    sale_detail = relationship("Sales_details", back_populates="sale")


class Sales_details(Base):
    __tablename__ = "sales_details"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    sale_id = Column(Integer,ForeignKey("sales.id",ondelete="CASCADE"), nullable=False)
    sale = relationship("Sales", back_populates="sale_detail")

    product_id = Column(Integer,ForeignKey("products.id",ondelete="SET NULL"), nullable=True)
    product = relationship("Product", back_populates="sale_detail")

    sale_amount = Column(Integer, nullable=False)