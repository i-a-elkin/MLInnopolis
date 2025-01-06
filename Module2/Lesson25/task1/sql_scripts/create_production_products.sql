CREATE TABLE production.products (
	product_id INT PRIMARY KEY,
	product_name VARCHAR (255),
	brand_id INT,
	category_id INT,
	model_year INT,
	list_price REAL,
	FOREIGN KEY (category_id) 
        REFERENCES production.categories (category_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (brand_id) 
        REFERENCES production.brands (brand_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);