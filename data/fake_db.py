from app.models.models import User3


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

users_db = {
    1: {'name': "John Doe", 'password': "12345"},
    2: {'name': "Jane Doe", 'password': "67890"},
    3: {'name': "Bob Smith", 'password': "24680"},
    4: {'name': "Mary Johnson", 'password': "13579"},
    5: {'name': "Tom Brown", 'password': "43210"},
    6: {'name': "Alice", 'password': "123"},
}

user_data = [User3(**{"username": "user1", "password": "pass_1"}), User3(**{"username": "user2", "password": "pass2"})]
