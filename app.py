import json
import os
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Product, CartItem, WishlistItem, Order, OrderItem

def create_app():
    app = Flask(__name__)
    
    # Configure SQLite database
    db_path = os.path.join(app.root_path, 'instance', 'zenithcart.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'zenith_platform_secret_gate_2.4.0'
    
    db.init_app(app)
    
    # Global context variables (for layout navbar)
    @app.context_processor
    def utility_processor():
        current_user = None
        cart_count = 0
        wishlist_count = 0
        
        if 'user_id' in session:
            current_user = db.session.get(User, session['user_id'])
            if current_user:
                cart_count = sum(item.quantity for item in current_user.cart_items)
                wishlist_count = len(current_user.wishlist_items)
                
        return dict(
            current_user=current_user,
            cart_count=cart_count,
            wishlist_count=wishlist_count
        )

    # Decorator to secure endpoints
    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to proceed.', 'error')
                return redirect(url_for('login_gate'))
            return f(*args, **kwargs)
        return decorated_function

    # Routes
    @app.route('/')
    def index():
        trending_products = Product.query.filter_by(is_trending=True).all()
        return render_template('index.html', trending_products=trending_products)

    @app.route('/login', methods=['GET', 'POST'])
    def login_gate():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            # Check if registration request or login request
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            
            if first_name and last_name: # Sign up trigger
                # Register
                existing = User.query.filter_by(email=email).first()
                if existing:
                    flash('Work email address already registered.', 'error')
                    return redirect(url_for('login_gate'))
                
                if not password or len(password) < 6:
                    flash('Password must be at least 6 characters long.', 'error')
                    return redirect(url_for('login_gate'))
                
                new_user = User(email=email, first_name=first_name, last_name=last_name)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                
                session['user_id'] = new_user.id
                flash('Account created successfully.', 'success')
                return redirect(url_for('dashboard'))
            else: # Log in trigger
                user = User.query.filter_by(email=email).first()
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    flash('Session initialized successfully.', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid credentials or access key.', 'error')
                    return redirect(url_for('login_gate'))
                    
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Session terminated successfully.', 'info')
        return redirect(url_for('index'))

    @app.route('/catalog')
    def catalog():
        category = request.args.get('category')
        search_query = request.args.get('search')
        sort_by = request.args.get('sort')
        
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
            
        if search_query:
            query = query.filter(Product.name.ilike(f'%{search_query}%') | Product.description.ilike(f'%{search_query}%'))
            
        if sort_by == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.price.desc())
        elif sort_by == 'rating':
            query = query.order_by(Product.rating.desc())
        else:
            query = query.order_by(Product.id.asc())
            
        products = query.all()
        categories = db.session.query(Product.category).distinct().all()
        categories = [c[0] for c in categories]
        
        return render_template('catalog.html', products=products, categories=categories, selected_category=category, search_query=search_query, sort_by=sort_by)

    @app.route('/product/<int:product_id>')
    def product_details(product_id):
        product = db.session.get(Product, product_id)
        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('catalog'))
            
        # Parse specifications
        specs_dict = {}
        if product.specs:
            try:
                specs_dict = json.loads(product.specs)
            except Exception:
                specs_dict = {}
                
        # Get related products in the same category
        related_products = Product.query.filter(Product.category == product.category, Product.id != product.id).limit(4).all()
        
        return render_template('product_details.html', product=product, specs=specs_dict, related_products=related_products)

    @app.route('/cart')
    @login_required
    def cart():
        user = db.session.get(User, session['user_id'])
        items = user.cart_items
        subtotal = sum(item.product.price * item.quantity for item in items)
        shipping = 0.00 if subtotal > 500.00 or subtotal == 0 else 15.00
        total = subtotal + shipping
        
        return render_template('cart.html', items=items, subtotal=subtotal, shipping=shipping, total=total)

    @app.route('/cart/add/<int:product_id>', methods=['POST'])
    @login_required
    def cart_add(product_id):
        user_id = session['user_id']
        quantity = int(request.form.get('quantity', 1))
        
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"status": "error", "message": "Product not found"}), 404
            
        if product.stock < quantity:
            return jsonify({"status": "error", "message": "Insufficient stock available"}), 400
            
        # Check if already in cart
        item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(item)
            
        db.session.commit()
        return jsonify({"status": "success", "message": "Product added to cart successfully", "cart_count": sum(i.quantity for i in db.session.get(User, user_id).cart_items)})

    @app.route('/cart/update/<int:item_id>', methods=['POST'])
    @login_required
    def cart_update(item_id):
        item = db.session.get(CartItem, item_id)
        if not item or item.user_id != session['user_id']:
            return jsonify({"status": "error", "message": "Item not found"}), 404
            
        qty = int(request.form.get('quantity', 1))
        if qty <= 0:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"status": "success", "message": "Item removed from cart"})
            
        if item.product.stock < qty:
            return jsonify({"status": "error", "message": f"Only {item.product.stock} items left in stock"}), 400
            
        item.quantity = qty
        db.session.commit()
        
        # Calculate new totals
        user = db.session.get(User, session['user_id'])
        items = user.cart_items
        subtotal = sum(i.product.price * i.quantity for i in items)
        shipping = 0.00 if subtotal > 500.00 or subtotal == 0 else 15.00
        total = subtotal + shipping
        
        return jsonify({
            "status": "success",
            "message": "Cart updated",
            "item_subtotal": f"₹{item.product.price * item.quantity:,.2f}",
            "subtotal": f"₹{subtotal:,.2f}",
            "shipping": f"₹{shipping:,.2f}",
            "total": f"₹{total:,.2f}",
            "cart_count": sum(i.quantity for i in items)
        })

    @app.route('/cart/delete/<int:item_id>', methods=['POST'])
    @login_required
    def cart_delete(item_id):
        item = db.session.get(CartItem, item_id)
        if not item or item.user_id != session['user_id']:
            flash('Item not found in cart.', 'error')
            return redirect(url_for('cart'))
            
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart.', 'info')
        return redirect(url_for('cart'))

    @app.route('/wishlist')
    @login_required
    def wishlist():
        user = db.session.get(User, session['user_id'])
        items = user.wishlist_items
        return render_template('wishlist.html', items=items)

    @app.route('/wishlist/add/<int:product_id>', methods=['POST'])
    @login_required
    def wishlist_add(product_id):
        user_id = session['user_id']
        
        # Check if already in wishlist
        item = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if item:
            return jsonify({"status": "success", "message": "Product is already in your wishlist"})
            
        item = WishlistItem(user_id=user_id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Product saved to wishlist"})

    @app.route('/wishlist/remove/<int:item_id>', methods=['POST'])
    @login_required
    def wishlist_remove(item_id):
        item = db.session.get(WishlistItem, item_id)
        if not item or item.user_id != session['user_id']:
            flash('Item not found in wishlist.', 'error')
            return redirect(url_for('wishlist'))
            
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from wishlist.', 'info')
        return redirect(url_for('wishlist'))

    @app.route('/wishlist/move-to-cart/<int:item_id>', methods=['POST'])
    @login_required
    def wishlist_move_to_cart(item_id):
        wishlist_item = db.session.get(WishlistItem, item_id)
        if not wishlist_item or wishlist_item.user_id != session['user_id']:
            flash('Item not found in wishlist.', 'error')
            return redirect(url_for('wishlist'))
            
        product_id = wishlist_item.product_id
        
        # Check if stock exists
        product = db.session.get(Product, product_id)
        if product.stock < 1:
            flash(f'{product.name} is currently out of stock.', 'error')
            return redirect(url_for('wishlist'))
            
        # Add to cart
        cart_item = CartItem.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=session['user_id'], product_id=product_id, quantity=1)
            db.session.add(cart_item)
            
        # Remove from wishlist
        db.session.delete(wishlist_item)
        db.session.commit()
        
        flash(f'Moved {product.name} to cart.', 'success')
        return redirect(url_for('wishlist'))

    @app.route('/checkout')
    @login_required
    def checkout():
        user = db.session.get(User, session['user_id'])
        items = user.cart_items
        if not items:
            flash('Your cart is empty.', 'error')
            return redirect(url_for('cart'))
            
        subtotal = sum(item.product.price * item.quantity for item in items)
        shipping = 0.00 if subtotal > 500.00 else 15.00
        total = subtotal + shipping
        
        return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping, total=total)

    @app.route('/checkout/process', methods=['POST'])
    @login_required
    def checkout_process():
        user = db.session.get(User, session['user_id'])
        cart_items = user.cart_items
        if not cart_items:
            return jsonify({"status": "error", "message": "Your cart is empty"}), 400
            
        # Verify card number and capture checkout forms
        card_number = request.form.get('card_number', '').strip()
        card_expiry = request.form.get('card_expiry', '').strip()
        card_cvc = request.form.get('card_cvc', '').strip()
        
        if not card_number or not card_expiry or not card_cvc:
            return jsonify({"status": "error", "message": "Payment credentials missing."}), 400
            
        # Generate mock transaction security logs
        logs = []
        logs.append("[SYS] INITIALIZING ZENITH SECURITY PROTOCOL V.4.0...")
        logs.append(f"[SYS] TRANSACTION ATTEMPT: USER_ID={user.id} EMAIL={user.email}")
        logs.append("[SYS] SECURE SHARDING HANDSHAKE OVER TLS 1.3... SUCCESS")
        
        # Simulating key validation
        logs.append("[CRYPT] VERIFYING GATEWAY ENCRYPTION SHIELD KEY...")
        logs.append("[CRYPT] SHIELD KEY CERTIFIED: PROTOCOL=AES-256-GCM")
        
        # Check stock validity
        for item in cart_items:
            if item.product.stock < item.quantity:
                logs.append(f"[ERROR] STOCK COLLISION: PRODUCT={item.product.sku} REQUIRED={item.quantity} AVAILABLE={item.product.stock}")
                return jsonify({
                    "status": "error",
                    "message": f"Stock collision: {item.product.name} does not have enough inventory.",
                    "logs": logs
                }), 400
                
        # Deduct stock and compile order
        subtotal = sum(i.product.price * i.quantity for i in cart_items)
        shipping = 0.00 if subtotal > 500.00 else 15.00
        total = subtotal + shipping
        
        order_number = f"ZNT-{random.randint(10000, 99999)}"
        order = Order(order_number=order_number, user_id=user.id, total_price=total)
        db.session.add(order)
        
        logs.append(f"[DB] COMPILING RECEIPT INVOICE {order_number}...")
        
        for item in cart_items:
            # Deduct stock
            item.product.stock -= item.quantity
            # Create OrderItem
            order_item = OrderItem(order_id=order.id, product_id=item.product_id, price=item.product.price, quantity=item.quantity)
            db.session.add(order_item)
            # Remove CartItem
            db.session.delete(item)
            logs.append(f"[DB] SEEDED RECEIPT ITEM: SKU={item.product.sku} PRICE={item.product.price} QTY={item.quantity}")
            
        db.session.commit()
        logs.append(f"[GATEWAY] PCI-DSS BANK COMPLIANCE TRANSACTION PIPELINE OPENED...")
        logs.append(f"[GATEWAY] TRANSACTION SETTLED. TRANSACTION_ID={order_number}_TXN")
        logs.append(f"[SYS] SESSION COMPLETED WITH STATUS SUCCESS.")
        
        return jsonify({
            "status": "success",
            "message": "Payment processed successfully.",
            "order_number": order_number,
            "logs": logs
        })

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = db.session.get(User, session['user_id'])
        recent_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).limit(3).all()
        return render_template('dashboard.html', user=user, recent_orders=recent_orders)

    @app.route('/orders')
    @login_required
    def orders():
        user = db.session.get(User, session['user_id'])
        user_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        return render_template('orders.html', orders=user_orders)

    @app.route('/orders/<order_number>')
    @login_required
    def order_details(order_number):
        order = Order.query.filter_by(order_number=order_number).first()
        if not order or order.user_id != session['user_id']:
            flash('Order not found.', 'error')
            return redirect(url_for('orders'))
            
        subtotal = sum(item.price * item.quantity for item in order.items)
        shipping = 0.00 if subtotal > 500.00 else 15.00
        total = subtotal + shipping
        
        return render_template('order_details.html', order=order, subtotal=subtotal, shipping=shipping, total=total)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
