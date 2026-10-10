-- =============================================================================
-- E-Commerce PostgreSQL Schema
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Products
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    id             VARCHAR(50)    PRIMARY KEY,
    name           VARCHAR(255)   NOT NULL,
    category       VARCHAR(100)   NOT NULL,
    price          NUMERIC(10, 2) NOT NULL,
    description    TEXT,
    in_stock       BOOLEAN        NOT NULL DEFAULT TRUE,
    stock_quantity INTEGER        NOT NULL DEFAULT 0,
    rating         NUMERIC(3, 1),
    image_url      TEXT
);

-- ---------------------------------------------------------------------------
-- Customers
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS customers (
    id             VARCHAR(50)  PRIMARY KEY,
    name           VARCHAR(255) NOT NULL,
    email          VARCHAR(255) UNIQUE NOT NULL,
    phone          VARCHAR(50),
    loyalty_points INTEGER      NOT NULL DEFAULT 0,
    member_since   TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Orders
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS orders (
    id              VARCHAR(50)    PRIMARY KEY,
    customer_id     VARCHAR(50)    NOT NULL REFERENCES customers(id),
    total_amount    NUMERIC(10, 2) NOT NULL,
    status          VARCHAR(50)    NOT NULL DEFAULT 'pending',
    tracking_number VARCHAR(100),
    -- shipping address (flattened to avoid a separate join for every order read)
    street          VARCHAR(255)   NOT NULL,
    city            VARCHAR(100)   NOT NULL,
    state           VARCHAR(100)   NOT NULL,
    zip_code        VARCHAR(20)    NOT NULL,
    country         VARCHAR(100)   NOT NULL DEFAULT 'USA',
    created_at      TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status      ON orders(status);

-- ---------------------------------------------------------------------------
-- Order Items
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS order_items (
    id           SERIAL         PRIMARY KEY,
    order_id     VARCHAR(50)    NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id   VARCHAR(50)    NOT NULL REFERENCES products(id),
    product_name VARCHAR(255)   NOT NULL,
    quantity     INTEGER        NOT NULL CHECK (quantity > 0),
    price        NUMERIC(10, 2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- ---------------------------------------------------------------------------
-- Shipping Rates
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS shipping_rates (
    type VARCHAR(50)    PRIMARY KEY,
    name VARCHAR(255)   NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,
    days VARCHAR(20)    NOT NULL
);

-- ---------------------------------------------------------------------------
-- Tracking Info
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tracking_info (
    tracking_number    VARCHAR(100) PRIMARY KEY,
    status             VARCHAR(50)  NOT NULL,
    current_location   VARCHAR(255) NOT NULL,
    estimated_delivery DATE
);

-- ---------------------------------------------------------------------------
-- Tracking Events (history per tracking number)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tracking_events (
    id               SERIAL       PRIMARY KEY,
    tracking_number  VARCHAR(100) NOT NULL REFERENCES tracking_info(tracking_number) ON DELETE CASCADE,
    event_timestamp  VARCHAR(50)  NOT NULL,
    location         VARCHAR(255) NOT NULL,
    status           VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tracking_events_number ON tracking_events(tracking_number);
