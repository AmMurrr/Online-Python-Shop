from sqlalchemy.orm import Session
from app.models.models import Cart, CartItem, Product
from app.schemas.carts import CartUpdate, CartCreate
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
# from app.core.security import get_current_user


class CartService:
    # Get All Carts
    @staticmethod
    def get_all_carts( db: Session):

        carts = db.query(Cart).all()
        message = f"Carts"
        return ResponseHandler.success(message, carts)

    # Get A Cart By ID
    @staticmethod
    def get_cart(user_id, db: Session):#, cart_id: int):   ###Cart.id == cart_idd,
        cart = db.query(Cart).filter( Cart.user_id == user_id).first()
        if not cart:
            ResponseHandler.not_found_error("User Cart", user_id)
        return ResponseHandler.get_single_success("cart", user_id, cart)

    # Create a new Cart
    @staticmethod
    def create_cart(user_id, db: Session, cart: CartCreate):
    
        cart_dict = cart.model_dump()

        cart_items_data = cart_dict.pop("cart_items", [])
        cart_items = []
        total_amount = 0
        for item_data in cart_items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            product = db.query(Product).filter(Product.id == product_id).first() 
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            subtotal = quantity * product.price 
            cart_item = CartItem(product_id=product_id, quantity=quantity, subtotal=subtotal)
            total_amount += subtotal

            cart_items.append(cart_item)
        cart_db = Cart(cart_items=cart_items, user_id=user_id, total_amount=total_amount, **cart_dict)
        db.add(cart_db)
        db.commit()
        db.refresh(cart_db)
        return ResponseHandler.create_success("Cart", cart_db.id, cart_db)

    # Update Cart & CartItem
    @staticmethod
    def update_cart(user_id, db: Session, updated_cart: CartUpdate):
      

        cart = db.query(Cart).filter( Cart.user_id == user_id).first()
        if not cart:
            return ResponseHandler.not_found_error("Cart", user_id)

        # Delete existing cart_items
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

        for item in updated_cart.cart_items:
            product_id = item.product_id
            quantity = item.quantity

            product = db.query(Product).filter(Product.id == product_id).first() 
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            subtotal = quantity * product.price * (product.discount_percentage / 100)

            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                subtotal=subtotal
            )
            db.add(cart_item)

        cart.total_amount = sum(item.subtotal for item in cart.cart_items)

        db.commit()
        db.refresh(cart)
        return ResponseHandler.update_success("cart", cart.id, cart)

    # Delete Both Cart and CartItems
    @staticmethod
    def delete_cart(user_id, db: Session):
     
        cart = (
            db.query(Cart)
            .options(joinedload(Cart.cart_items).joinedload(CartItem.product))
            .filter( Cart.user_id == user_id)
            .first()
        )
        if not cart:
            ResponseHandler.not_found_error("Cart", user_id)

        for cart_item in cart.cart_items:
            db.delete(cart_item)

        db.delete(cart)
        db.commit()
        return ResponseHandler.delete_success("Cart", user_id, cart)
