CREATE TABLE sales.orders (
	order_id INT PRIMARY KEY,
	customer_id INT,
	order_status INT,
	order_date DATE,
	required_date DATE,
	shipped_date DATE,
	store_id INT,
	staff_id INT,
	FOREIGN KEY (customer_id) 
        REFERENCES sales.customers (customer_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (store_id) 
        REFERENCES sales.stores (store_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (staff_id) 
        REFERENCES sales.staffs (staff_id) 
        ON DELETE NO ACTION ON UPDATE NO ACTION
);