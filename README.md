# ZenithCart

**ZenithCart** is a modern, high-velocity digital flagship commerce platform. Built with a secure Python-driven architecture and a highly polished, performance-oriented aesthetic, ZenithCart provides a premium retail experience engineered for absolute velocity.

![ZenithCart](https://lh3.googleusercontent.com/aida/AP1WRLufguzk0Yu1Jfoq3HXqW4-Bs-hf1PiBpR9IzI3f7hQaLDtYvheCbD9-jzKmQErjYLKHlSL3ExCQgBZafP-3k_18nsogMVB_ZGsH-xb-U6txAB-sLoeZg1xjKMuCKkOywmS-BB4pGApY40cgVEZJhzO8ldEKxLO9iHOzfNc7c90VbO6B3FusVQXIE7kBh7dpZ-WqNA003tmDkPZVHWibUGqMhiK9BYWoZ1GQwxDqXshS9fvVnYJ4RY571A)

## 🚀 Key Features

*   **Precision Commerce Infrastructure:** Blazing fast navigation and product exploration with a sleek, dark-themed UI.
*   **Dynamic Product Catalog:** Filter products by category, search by name or description, and sort by price or rating.
*   **User Accounts & Authentication:** Secure session management and credential encryption.
*   **Wishlist & Cart System:** Save products for later or add them to the cart. Features asynchronous cart updates and real-time UI synchronization.
*   **Secure Checkout & Order History:** A seamless checkout flow with automated order tracking and user history.
*   **Responsive Design:** Fully responsive layout built with Tailwind CSS, ensuring a perfect experience across desktops, tablets, and mobile devices.

## 🛠️ Technology Stack

*   **Backend Engine:** Python, Flask, Flask-SQLAlchemy
*   **Database:** SQLite (Default, scalable to PostgreSQL/MySQL via SQLAlchemy)
*   **Frontend UI:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript
*   **Design Language:** High-craft modern dark mode, glassmorphism, fluid micro-animations

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/AbhinavKumar36/ZenithCart.git
    cd ZenithCart
    ```

2.  **Create and Activate a Virtual Environment**
    ```powershell
    # Windows
    python -m venv .venv
    .venv\Scripts\Activate.ps1

    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    If a `requirements.txt` is present:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Essential packages include `Flask` and `Flask-SQLAlchemy`)*

4.  **Initialize & Seed the Database**
    Populate the store with default products and the test user account:
    ```bash
    python seed_db.py
    ```
    This creates an `instance/store.db` file and generates sample data, including the default engineer account:
    *   **Email:** `engineer@zenith.tech`
    *   **Password:** `zenithkey123`

5.  **Run the Application Server**
    ```bash
    python app.py
    ```
    The application will be accessible locally at `http://127.0.0.1:5000`.

## 📂 Project Structure

```text
ZenithCart/
├── app.py                  # Core application, routing, and controller logic
├── models.py               # SQLAlchemy database models (User, Product, Cart, Order, etc.)
├── seed_db.py              # Script to populate the database with default data
├── static/                 # Static assets (favicons, etc.)
└── templates/              # Jinja2 HTML Templates
    ├── base.html           # Master layout template
    ├── index.html          # Storefront / Hero page
    ├── catalog.html        # Product browsing and filtering
    ├── product_details.html# Individual product view
    ├── cart.html           # Shopping cart
    ├── checkout.html       # Order confirmation and payment
    ├── orders.html         # User's order history
    ├── wishlist.html       # Saved items
    └── login.html          # Authentication gateway
```

## 🔐 Security Protocols

ZenithCart relies on the following core security principles:
*   Session-based authentication leveraging Flask's encrypted cookie system.
*   Secure password hashing (Werkzeug Security).
*   Guarded endpoints with the `@login_required` decorator.

---
*Engineered by the ZenithCart Development Team.*
