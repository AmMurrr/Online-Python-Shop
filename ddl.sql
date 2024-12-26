-- Create the 'user_roles' enum type
CREATE TYPE user_roles AS ENUM ('admin', 'user');

-- Create the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    role user_roles DEFAULT 'user' NOT NULL
);

-- Create the 'categories' table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

-- Create the 'products' table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    price INTEGER NOT NULL,
    discount_percentage FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    brand VARCHAR NOT NULL,
    images TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE
);

-- Create the 'carts' table
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    total_amount FLOAT NOT NULL
);

-- Create the 'cart_items' table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    subtotal FLOAT NOT NULL
);

CREATE TABLE sales(
    "id" SERIAL PRIMARY KEY,
    "sale_date" TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    "total_cost" FLOAT NOT NULL,
    "user_id" BIGINT REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE sales_details (
    id SERIAL PRIMARY KEY,
    sale_id BIGINT NOT NULL REFERENCES sales(id) ON DELETE CASCADE,                
    product_id BIGINT REFERENCES products(id) ON DELETE SET NULL,             
    sale_amount BIGINT NOT NULL

);