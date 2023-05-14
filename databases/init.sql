CREATE TABLE memberships (
    membership_id VARCHAR(100) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    date_of_birth VARCHAR(20) NOT NULL,
    mobile_no VARCHAR(20) NOT NULL
);

CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(100) NOT NULL
);

CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_cost FLOAT NOT NULL,
    item_weight FLOAT NOT NULL,
    deleted_at TIMESTAMP NULL
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    membership_id VARCHAR(100) REFERENCES memberships(membership_id),
    manufacturer_id INT REFERENCES manufacturers(manufacturer_id),
    total_items_cost FLOAT NOT NULL,
    total_items_weight FLOAT NOT NULL,
    transaction_status VARCHAR(100) NOT NULL
);

CREATE TABLE transacted_items (
    transaction_id INT REFERENCES transactions(transaction_id),
    item_id INT REFERENCES items(item_id),
    quantity INT
);