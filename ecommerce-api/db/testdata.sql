INSERT INTO users (username, email, hashed_password, is_seller) VALUES
('alice', 'alice@example.com', 'hashedpwd1', TRUE),
('bob', 'bob@example.com', 'hashedpwd2', TRUE),
('charlie', 'charlie@example.com', 'hashedpwd3', FALSE),
('dave', 'dave@example.com', 'hashedpwd4', FALSE),
('eve', 'eve@example.com', 'hashedpwd5', TRUE),
('frank', 'frank@example.com', 'hashedpwd6', TRUE),
('grace', 'grace@example.com', 'hashedpwd7', FALSE),
('heidi', 'heidi@example.com', 'hashedpwd8', FALSE),
('ivan', 'ivan@example.com', 'hashedpwd9', TRUE),
('judy', 'judy@example.com', 'hashedpwd10', TRUE);


INSERT INTO categories (name, description) VALUES
('Electronics', 'Devices and gadgets'),
('Fashion', 'Clothing and accessories'),
('Books', 'Fiction and non-fiction'),
('Home', 'Furniture and decor'),
('Toys', 'Toys and games'),
('Sports', 'Sports equipment'),
('Health', 'Health and wellness products'),
('Automotive', 'Car accessories'),
('Food', 'Groceries and snacks'),
('Art', 'Artworks and supplies');


INSERT INTO products (name, description, price, seller_id, category_id, stock) VALUES
('Smartphone', 'Latest model smartphone', 699.99, 1, 1, 50),
('Laptop', 'High-performance laptop', 999.99, 1, 1, 18),
('T-Shirt', 'Cotton T-shirt', 19.99, 2, 2, 10),
('Cookbook', 'Recipes from around the world', 29.99, 3, 3, 14),
('Sofa', 'Comfortable three-seater', 299.99, 4, 4, 90),
('Doll', 'Cute doll for kids', 14.99, 5, 5, 33),
('Basketball', 'Official size basketball', 24.99, 6, 6, 20),
('Vitamins', 'Multivitamin supplements', 15.99, 7, 7, 23),
('Car Cover', 'Waterproof car cover', 49.99, 8, 8, 10),
('Organic Coffee', 'Freshly roasted organic coffee', 14.99, 9, 9, 17);


INSERT INTO orders (buyer_id, status, total_price) VALUES
(3, 'PENDING', 719.98),
(4, 'DELIVERED', 1049.98),
(5, 'SHIPPED', 39.98),
(6, 'CANCELLED', 299.99),
(7, 'PENDING', 14.99),
(8, 'DELIVERED', 24.99),
(9, 'SHIPPED', 15.99),
(10, 'CANCELLED', 49.99),
(3, 'PENDING', 14.99),
(4, 'SHIPPED', 29.99);


INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 2),
(4, 5, 1),
(5, 6, 1),
(6, 7, 1),
(7, 8, 1),
(8, 9, 1),
(9, 10, 1),
(10, 4, 1);


INSERT INTO reviews (order_id, reviewer_id, rating, comment) VALUES
(1, 2, 5, 'Excellent product, highly recommend!'),
(2, 3, 4, 'Good quality, but delivery was a bit slow.'),
(3, 4, 3, 'Average experience, not very satisfied with the product.'),
(4, 5, 5, 'Amazing service and great value for money!'),
(5, 6, 4, 'Pretty good, but there is room for improvement.'),
(6, 7, 2, 'The product did not match the description.'),
(7, 8, 1, 'Terrible experience, completely dissatisfied.'),
(8, 9, 5, 'Superb! Will definitely buy again.'),
(9, 10, 4, 'Great product, but packaging could be better.'),
(10, 11, 5, 'Fantastic quality and fast delivery!');


