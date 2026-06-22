import json
import os
from app import create_app
from models import db, Product, User

def seed():
    app = create_app()
    with app.app_context():
        # Ensure clean slate
        db.drop_all()
        db.create_all()
        
        products = [
            {
                "name": "Zenith Aero V1",
                "sku": "ZNT-AERO-V1",
                "category": "electronics",
                "price": 1299.00,
                "description": "Pro-grade flight stabilization and 8K imaging. Engineered with active obstacle avoidance and standard 45-minute battery life.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBeYEmk-5uVs5peApIJKyS9tr6O8Y3dNsn7YVdbx_k2GVtBJ5RkI6RK79w_qU6wDUaGcXVhAKhwVwGS3wmGV_YLbFhaK3oht0tYJOnayl5JV4OzWMjXM6BMovy-9leyGKFE2zaRNxXqIsbS57VzatV8MVW12-2UJ3RTOASUeQi9vftXQmVo3hzbRukICb9oE7g893YLw8XarbfUf0KC0HcireGEkb_4zLzVeYsfpUd3TIBFMJrfHOcWiJ6Kztv2Hf5pno0JF1lqHYg",
                "is_trending": True,
                "rating": 4.9,
                "stock": 5,
                "specs": json.dumps({
                    "Camera Resolution": "8K UHD @ 60fps",
                    "Flight Time": "45 Minutes",
                    "Range": "12 Kilometers",
                    "Weight": "750g",
                    "Obstacle Avoidance": "360-Degree Spherical"
                })
            },
            {
                "name": "Flux Key Pro",
                "sku": "ZNT-FLUX-KEY",
                "category": "electronics",
                "price": 249.00,
                "description": "Mechanical precision with low-latency Bluetooth 5.2. Hot-swappable tactile switches with dark translucent custom chassis.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuD1EjeHaZmuNmgKTRLNYGMZqyTzn3ZczitXUuZ1S692pYtK6056rLlQDcu4Ix-0HqHCQKmlfoWkut-E9vjo9_vVcF-2qSMKBlyX9AW4MrMjzVC1IV_CP39O0UjjN-jTedVQQ4JyKaowK5w4MfyYW22wAjltq9Xz2AEuLq5wlJuL941sCzJECGMgcRyW-arMGCeagpjn5gcx9d5bnSwSC9EcMud-0DXs3xQilOQH4_CdmCRFqgTMXVtRlY5oJ_UKTz4YYTDOODvxYjA",
                "is_trending": True,
                "rating": 4.7,
                "stock": 15,
                "specs": json.dumps({
                    "Switch Type": "Tactile Violet Switches (Hot-Swappable)",
                    "Connectivity": "Bluetooth 5.2 / 2.4GHz / USB-C",
                    "Battery Life": "Up to 200 Hours (RGB Off)",
                    "Layout": "75% compact profile",
                    "Keycaps": "Double-shot PBT cherry profile"
                })
            },
            {
                "name": "Chronos S3",
                "sku": "ZNT-CHRONOS-S3",
                "category": "lifestyle",
                "price": 449.00,
                "description": "Bespoke timekeeping with biometric health tracking. Encased in grade 5 titanium with high-resolution sapphire glass display.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDPCjlJVLes9OwL4tfNUzI1nxpgQzo3vRMXMWym-4koVwiSWw0RGF11fjzcfG3AZ2jLLVD1AxHjTc3T7QDGPisTwEpeRB8UJQscgaiPaWrrbFUSHrPjPwgPQ629IrPm92mWXkwnUKw5MKB2cBKTdSnJyPcO_gKZK0q4dM9PdMGQM8qv64O8SqoCUrqCPnkkgM46NaRlCSuBtP3SoT0vQCXCKbDS1ubuywv64N05nSvrFmQUSB3lCZYwjxoK43NL2YRTGpkBJfYE5QY",
                "is_trending": True,
                "rating": 4.8,
                "stock": 8,
                "specs": json.dumps({
                    "Chassis Material": "Grade 5 Titanium",
                    "Sensors": "ECG, Optical Heart Rate, SpO2, Accelerometer",
                    "Water Resistance": "50m (5 ATM)",
                    "Screen Type": "1.4-inch AMOLED Sapphire Glass",
                    "Battery Life": "Up to 7 Days"
                })
            },
            {
                "name": "Sonic Ridge ANC",
                "sku": "ZNT-SONIC-RIDGE",
                "category": "electronics",
                "price": 399.00,
                "description": "Pure acoustic engineering with adaptive active noise isolation. Features customized planar magnetic drivers for precise sound separation.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCQ-A3B4UUEye6KeXAnkYnlTNsbVUbd7Du8i0iwqeAP_vefDSm6wsmAqWs_5SJ9K0_GdkFkXIAMEJ07uopGnq2Uu5VlD_AGK6G96xlktKo4i1TEPxB2bwutVy1oh638dF2Gm8i33cy1ymAzCTo4X7LtEuZiFo5g-wGIMvQ-AZaupc9-oiI06tB0kFPerRBS3__PqLk6MrV_kIybNOk-uhm-iojWamefL6CIydZXRCzvlLmNseKfVCJFs54yfXH4x9Q8EPxA-8Oen-M",
                "is_trending": True,
                "rating": 4.6,
                "stock": 12,
                "specs": json.dumps({
                    "Driver Type": "40mm Planar Magnetic",
                    "Noise Isolation": "Hybrid Active (up to 40dB)",
                    "Battery Life": "40 Hours with ANC On",
                    "Codecs Supported": "LDAC, AAC, SBC",
                    "Weight": "290g"
                })
            },
            {
                "name": "Apex Shell Jacket",
                "sku": "ZNT-APEX-SHELL",
                "category": "technical_apparel",
                "price": 349.00,
                "description": "Waterproof, wind-resistant breathable membrane. Features laser-cut vents, fully taped seams, and magnetic hood adjustments for modern urban resilient wear.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuB2N-vUmDMvbxNys4WzmF2R-OT-T1aoQ5qoVeIMvK4YGC67XHx_iiF_nCbDjdDN9NGptMZpQ1D2RmCCwfMlp_COIz2csop-6icaTlG1d-GMpUKKacH94CiOmobOSLJcyHJFXCATnX8SYvBLxycwPrczr9wfaWfaC55oN7wJIEYTHvy446ljcyyYCrgPWvwiidsKVv60IlI-tENdyyy3XwV_u5V7PpIMZX-c8ldnTgTTKfcOmF2iab8Y3uYjaSWDUTF3G0zXxqactuU",
                "is_trending": False,
                "rating": 4.8,
                "stock": 20,
                "specs": json.dumps({
                    "Fabric": "3-Layer Graphene Membrane",
                    "Waterproof Rating": "20,000mm",
                    "Breathability": "15,000g/m²/24h",
                    "Pockets": "4 external storm zip pockets, 1 internal secure pocket",
                    "Fit": "Ergonomic modular profile"
                })
            },
            {
                "name": "Vector Cargo Pants",
                "sku": "ZNT-VECTOR-CARGO",
                "category": "technical_apparel",
                "price": 189.00,
                "description": "Reinforced seams, water-resistant quick-dry technical cargo trousers with dynamic modular expansion pockets.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDPt67A7iBAGYzk5CaHUyxiXxdqF4kH4GFeWkUjdY8WR1JY9ArI6rywUvZ3urJKVRlFEJNtMm7At-C4OmNQFbz7Slk5NcYmDtGwY7zB0NZQD7Nc9VqMRcLNKW_gpV_4dA-P2e73Itowax-nw7gKffGBeFTgtzKY5oie0MHN3pqIWgeMPqwfSv8ysuBIENjzLEBCU_bbONIeiaCZ6s_qCo4z92vEyvquqXFtD9CdX1G0RnbSLtzxAJmFeRPCeV-hHUFdnlXjcFR-5bc",
                "is_trending": False,
                "rating": 4.5,
                "stock": 25,
                "specs": json.dumps({
                    "Fabric": "Nylon-Spandex double weave DWR coated",
                    "Pockets": "2 front slant, 2 cargo side-expansion, 2 zip rear",
                    "Ankle cuff": "Adjustable magnetic snap system",
                    "Resilience": "Ripstop panel inserts"
                })
            },
            {
                "name": "Apex Smart Thermostat",
                "sku": "ZNT-APEX-THERM",
                "category": "home",
                "price": 299.00,
                "description": "Neural network climate optimizer with dark glass interface. Real-time air quality indexing and multizone control algorithms.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuB3i6wN6dVBC1DKLNrliO78NP3Bedvz3F0Ntuxj5aGWIQmZV2oor9ubQfWlxq5zN5ZbU15fHv9c-xSCQUMoJOVjFnlg7rq85y1V3q3ItOLHoQMjhzFH99mut-9OlyF7tU2b0gqMqhHh6YXOnwLxG3UxMc_0qlTlu3uLl0yoRIrihlwSYKNK66wY8nhhH5Ilf2T8IGhkSZrCGelWcelOETJHS-hIN83ihwiaWvkYYj2NeZ4OwDZ0ELBGqYwX7iB8VV464epLsQxaf30",
                "is_trending": False,
                "rating": 4.7,
                "stock": 10,
                "specs": json.dumps({
                    "Display": "2.8-inch Curved Oled Glass",
                    "Connectivity": "Wi-Fi 6, Zigbee, Thread",
                    "AI engine": "Dynamic occupancy scheduling",
                    "Installation": "Standard 24V C-wire system"
                })
            },
            {
                "name": "Minimalist Desk Light",
                "sku": "ZNT-STEEL-LAMP",
                "category": "home",
                "price": 159.00,
                "description": "Anodized aluminum frame with dimmable high-CRI led source. Built-in Qi charging pad at the slate base.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBeYEmk-5uVs5peApIJKyS9tr6O8Y3dNsn7YVdbx_k2GVtBJ5RkI6RK79w_qU6wDUaGcXVhAKhwVwGS3wmGV_YLbFhaK3oht0tYJOnayl5JV4OzWMjXM6BMovy-9leyGKFE2zaRNxXqIsbS57VzatV8MVW12-2UJ3RTOASUeQi9vftXQmVo3hzbRukICb9oE7g893YLw8XarbfUf0KC0HcireGEkb_4zLzVeYsfpUd3TIBFMJrfHOcWiJ6Kztv2Hf5pno0JF1lqHYg",
                "is_trending": False,
                "rating": 4.3,
                "stock": 18,
                "specs": json.dumps({
                    "Power Draw": "12W Led",
                    "Color Temp": "2700K - 6500K continuous adjust",
                    "Base Feature": "15W Qi Wireless Charger",
                    "Material": "Anodized Space Gray Aluminum"
                })
            },
            {
                "name": "Technical Merino Hoodie",
                "sku": "ZNT-MERINO-HD",
                "category": "technical_apparel",
                "price": 160.00,
                "description": "Odor-resistant fine merino wool active layer with reinforced Cordura elbow patches. Outstanding thermal insulation.",
                "image_url": "https://lh3.googleusercontent.com/aida/AP1WRLstGB745sLXLQuJ3ZoVK_B0YKHx-udP7PjDBc6w_kyfkFgKXPr3sWMr3qKiYa3yRx7gOrTzwVMYNyOldzLlvcIVitAP1TaivLVuRFxKjRGIkbigQtMAv6mmSvIY5G3MVxn14MJRjTwYdSuxTW6q3WpJmmYBfsaZ-janxCM5dAv-sB3iCvZt-uuERtKtoYm3T2YVgna2UKu6bsPPOKH4H20nRr0WvVJIMYUrXb0Olwegmg1b4lIfnT0H0F4",
                "is_trending": False,
                "rating": 4.6,
                "stock": 30,
                "specs": json.dumps({
                    "Material Blend": "85% Merino Wool, 15% Cordura Nylon",
                    "Fabric Weight": "260 gsm",
                    "Pockets": "Double concealed side zip pockets",
                    "Elbow reinforcement": "1000D Cordura patches"
                })
            }
        ]
        
        for p_data in products:
            p = Product(**p_data)
            db.session.add(p)
            
        # Create a default test user
        test_user = User(
            email="engineer@zenith.tech",
            first_name="Linus",
            last_name="Torvalds"
        )
        test_user.set_password("zenithkey123")
        db.session.add(test_user)
        
        db.session.commit()
        print("Database seeded successfully with default test user (engineer@zenith.tech / zenithkey123) and 9 products.")

if __name__ == "__main__":
    seed()
