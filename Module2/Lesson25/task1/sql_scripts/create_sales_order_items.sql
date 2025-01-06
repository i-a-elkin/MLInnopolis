CREATE TABLE sales.order_items(
	order_id INT,
	item_id INT,
	product_id INT,
	quantity INT,
	list_price REAL,
	discount REAL,
	PRIMARY KEY (order_id, item_id),
	FOREIGN KEY (order_id) 
        REFERENCES sales.orders (order_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (product_id) 
        REFERENCES production.products (product_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);