CREATE DATABASE IF NOT EXISTS servicios_compras
    CHARACTER SET = 'utf8'
    COLLATE = 'utf8_general_ci';

USE servicios_pedidos;

CREATE TABLE IF NOT EXISTS pedidos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Direccion VARCHAR(50),
    Estado VARCHAR(255),
    Ubicacion VARCHAR(255),
    Metodo_Pago VARCHAR(255),
    Total_Pagar VARCHAR(255)
) ENGINE=InnoDB;