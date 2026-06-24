CREATE SCHEMA IF NOT EXISTS `stock_db` DEFAULT CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS `stock_db`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `quantity` INT NOT NULL,
  `minimal_stock` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `stock_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `login` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `stock_db`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` ENUM('buy', 'sell') NOT NULL,
  `quantity` INT NOT NULL,
  `date` DATE NOT NULL,
  `users_id` INT NOT NULL,
  `products_id` INT NOT NULL,
  INDEX `fk_table1_products_idx` (`products_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_table1_products`
    FOREIGN KEY (`products_id`)
    REFERENCES `stock_db`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `stock_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE stock_db;

INSERT INTO users (name, login, password)
VALUES ('Admin', 'admin', '1234');
SELECT * FROM users;

INSERT INTO products (name, quantity, minimal_stock)
VALUES
('Bread', 50, 15),
('Cheese', 40, 10),
('Eggs', 60, 20);
SELECT * FROM products;

SELECT * FROM orders;