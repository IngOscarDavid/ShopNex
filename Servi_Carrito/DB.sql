CREATE DATABASE IF NOT EXISTS servicios_carrito
    CHARACTER SET = 'utf8'
    COLLATE = 'utf8_general_ci';

USE servicios_carrito;

CREATE TABLE IF NOT EXISTS carrito(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Codigo_Usuario VARCHAR(255),
    Codigo_Producto VARCHAR(255),
    Nombre VARCHAR(255),
    Precio VARCHAR(255),
    Imagen VARCHAR(255),
    Total VARCHAR(255)
) ENGINE=InnoDB;