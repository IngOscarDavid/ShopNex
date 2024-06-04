CREATE DATABASE IF NOT EXISTS servicios_catalogo
    CHARACTER SET = 'utf8'
    COLLATE = 'utf8_general_ci';

USE servicios_catalogo;

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Codigo VARCHAR(50),
    Nombre VARCHAR(255),
    Descripcion TEXT,
    Catalogo VARCHAR(50),
    Precio VARCHAR(50),
    Cantidad VARCHAR(50),
    Image VARCHAR(255),
    Descuento VARCHAR(50)
) ENGINE=InnoDB;
