-- =============================================================================
-- E-Commerce Seed Data
-- Run after schema.sql:  psql -d ecommerce -f schema.sql -f seed.sql
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Products
-- ---------------------------------------------------------------------------

INSERT INTO products (id, name, category, price, description, in_stock, stock_quantity, rating, image_url) VALUES
    ('PROD-001', 'Wireless Bluetooth Headphones', 'Electronics', 79.99,
     'Premium wireless headphones with noise cancellation',
     TRUE, 45, 4.5, 'https://example.com/headphones.jpg'),

    ('PROD-002', 'Laptop Stand Aluminum', 'Accessories', 39.99,
     'Ergonomic aluminum laptop stand',
     TRUE, 120, 4.7, 'https://example.com/stand.jpg'),

    ('PROD-003', 'USB-C Hub Adapter', 'Electronics', 29.99,
     '7-in-1 USB-C hub with HDMI and USB ports',
     TRUE, 200, 4.3, 'https://example.com/hub.jpg'),

    ('PROD-004', 'Mechanical Keyboard RGB', 'Electronics', 129.99,
     'Gaming mechanical keyboard with RGB lighting',
     FALSE, 0, 4.8, 'https://example.com/keyboard.jpg'),

    ('PROD-005', 'Wireless Mouse', 'Electronics', 24.99,
     'Ergonomic wireless mouse with programmable buttons',
     TRUE, 85, 4.4, 'https://example.com/mouse.jpg')
ON CONFLICT (id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Customers
-- ---------------------------------------------------------------------------

INSERT INTO customers (id, name, email, phone, loyalty_points, member_since) VALUES
    ('CUST-001', 'John Doe',   'john.doe@example.com',   '+1-555-0123', 2500, '2023-01-15 00:00:00'),
    ('CUST-002', 'Jane Smith', 'jane.smith@example.com', '+1-555-0456', 1200, '2023-06-20 00:00:00')
ON CONFLICT (id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Orders
-- ---------------------------------------------------------------------------

INSERT INTO orders (id, customer_id, total_amount, status, tracking_number,
                    street, city, state, zip_code, country, created_at, updated_at) VALUES
    ('ORD-12345', 'CUST-001', 79.99, 'shipped', 'TRK-789456123',
     '123 Main St', 'New York', 'NY', '10001', 'USA',
     NOW() - INTERVAL '3 days', NOW() - INTERVAL '12 hours'),

    ('ORD-67890', 'CUST-002', 79.98, 'processing', NULL,
     '456 Oak Ave', 'Los Angeles', 'CA', '90001', 'USA',
     NOW() - INTERVAL '1 day',  NOW() - INTERVAL '2 hours')
ON CONFLICT (id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Order Items
-- ---------------------------------------------------------------------------

INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES
    ('ORD-12345', 'PROD-001', 'Wireless Bluetooth Headphones', 1, 79.99),
    ('ORD-67890', 'PROD-002', 'Laptop Stand Aluminum',         2, 39.99);

-- ---------------------------------------------------------------------------
-- Shipping Rates
-- ---------------------------------------------------------------------------

INSERT INTO shipping_rates (type, name, cost, days) VALUES
    ('standard',  'Standard Shipping',  5.99,  '5-7'),
    ('express',   'Express Shipping',   15.99, '2-3'),
    ('overnight', 'Overnight Shipping', 29.99, '1')
ON CONFLICT (type) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Tracking Info
-- ---------------------------------------------------------------------------

INSERT INTO tracking_info (tracking_number, status, current_location, estimated_delivery) VALUES
    ('TRK-789456123', 'in_transit', 'Distribution Center - Chicago, IL', CURRENT_DATE + 2),
    ('TRK-123456789', 'delivered',  'Delivered',                          CURRENT_DATE - 1)
ON CONFLICT (tracking_number) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Tracking Events
-- ---------------------------------------------------------------------------

INSERT INTO tracking_events (tracking_number, event_timestamp, location, status) VALUES
    ('TRK-789456123', '2025-12-25 08:00', 'Origin - New York, NY',                 'Picked up'),
    ('TRK-789456123', '2025-12-26 14:30', 'Distribution Center - Chicago, IL',     'In transit'),
    ('TRK-123456789', '2025-12-20 09:00', 'Origin - Los Angeles, CA',              'Picked up'),
    ('TRK-123456789', '2025-12-21 16:45', 'Distribution Center - Phoenix, AZ',     'In transit'),
    ('TRK-123456789', '2025-12-22 11:30', 'Local Facility - San Diego, CA',        'Out for delivery'),
    ('TRK-123456789', '2025-12-22 15:20', 'San Diego, CA',                         'Delivered');
