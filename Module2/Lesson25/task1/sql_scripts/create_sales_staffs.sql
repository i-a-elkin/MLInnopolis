CREATE TABLE sales.staffs (
	staff_id INT PRIMARY KEY,
	first_name VARCHAR (50),
	last_name VARCHAR (50),
	email VARCHAR (255),
	phone VARCHAR (25),
	active INT,
	store_id INT,
	manager_id INT,
	FOREIGN KEY (store_id) 
        REFERENCES sales.stores (store_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (manager_id) 
        REFERENCES sales.staffs (staff_id) 
        ON DELETE NO ACTION ON UPDATE NO ACTION
);