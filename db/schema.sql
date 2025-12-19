create table if not exists meta (
    meta_id INTEGER PRIMARY KEY,
    meta_name VARCHAR(40) UNIQUE,
    meta_content VARCHAR(64)
);

create table if not exists category (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(40) UNIQUE
);

create table if not exists subcategory (
    subcategory_id INTEGER PRIMARY KEY,
    subcategory_name VARCHAR(40) UNIQUE,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

create table if not exists item (
    item_id INTEGER PRIMARY KEY,
    item_name VARCHAR(40),
    item_description VARCHAR(40),
    item_url VARCHAR(40),
    category_id INTEGER,
    subcategory_id INTEGER
);

create table if not exists local (
    local_id INTEGER PRIMARY KEY,
    label VARCHAR(40),
    zh VARCHAR(40)
);

create table if not exists admin (
    admin_id INTEGER PRIMARY KEY,
    admin_name VARCHAR(40) UNIQUE,
    admin_password_hash VARCHAR(64)
);
