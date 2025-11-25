create table meta (
    meta_id INTEGER PRIMARY KEY,
    meta_name VARCHAR(40) UNIQUE,
    meta_content VARCHAR(64)
);

create table category (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(40) UNIQUE
);

create table subcategory (
    subcategory_id INTEGER PRIMARY KEY,
    subcategory_name VARCHAR(40) UNIQUE,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

create table item (
    item_id INTEGER PRIMARY KEY,
    item_name VARCHAR(40),
    item_description VARCHAR(40),
    item_url VARCHAR(40),
    category_id INTEGER,
    subcategory_id INTEGER
);

create table local (
    local_id INTEGER PRIMARY KEY,
    label VARCHAR(40),
    zh VARCHAR(40)
);