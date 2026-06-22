import sys
from app import create_app
from models import db, User, Product

def test_routes():
    print("Initializing Flask test client...")
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    client = app.test_client()
    
    # 1. Test homepage loads successfully
    print("Testing GET '/' (Homepage)...")
    res = client.get('/')
    if res.status_code != 200:
        print(f"FAILED: GET '/' returned status code {res.status_code}")
        sys.exit(1)
    print("SUCCESS: GET '/' loaded successfully (200 OK)")

    # 2. Test catalog loads successfully
    print("Testing GET '/catalog'...")
    res = client.get('/catalog')
    if res.status_code != 200:
        print(f"FAILED: GET '/catalog' returned status code {res.status_code}")
        sys.exit(1)
    print("SUCCESS: GET '/catalog' loaded successfully (200 OK)")

    # 3. Test login gate loads successfully
    print("Testing GET '/login'...")
    res = client.get('/login')
    if res.status_code != 200:
        print(f"FAILED: GET '/login' returned status code {res.status_code}")
        sys.exit(1)
    print("SUCCESS: GET '/login' loaded successfully (200 OK)")

    # 4. Test login authentication
    print("Testing POST '/login' with correct test credentials...")
    res = client.post('/login', data=dict(
        email="engineer@zenith.tech",
        password="zenithkey123"
    ), follow_redirects=True)
    if res.status_code != 200:
        print(f"FAILED: POST '/login' authentication returned status code {res.status_code}")
        sys.exit(1)
    if b"Welcome back, Linus" not in res.data and b"Portal" not in res.data:
        print(f"FAILED: Login response did not contain dashboard elements. Data: {res.data[:200]}")
        sys.exit(1)
    print("SUCCESS: Logged in successfully, dashboard rendered!")

    # 5. Test invalid login credentials
    print("Testing POST '/login' with invalid credentials...")
    client.get('/logout')  # Clear active session from test 4
    res = client.post('/login', data=dict(
        email="engineer@zenith.tech",
        password="wrongpassword"
    ), follow_redirects=True)
    if b"Invalid credentials" not in res.data:
        print("FAILED: Did not receive invalid credentials warning message.")
        sys.exit(1)
    print("SUCCESS: Invalid credentials correctly rejected with flash message!")

    # 6. Test catalog filters
    print("Testing catalog category filter '/catalog?category=electronics'...")
    res = client.get('/catalog?category=electronics')
    if b"Zenith Aero V1" not in res.data:
        print("FAILED: Category filter failed to show electronics items.")
        sys.exit(1)
    print("SUCCESS: Catalog category filters verified successfully!")

    print("\nALL PLATFORM TESTS PASSED SUCCESSFULLY! ZENITHCART CORE IS STABLE.")

if __name__ == "__main__":
    test_routes()
