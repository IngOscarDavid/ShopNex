CREATE DATABASE IF NOT EXISTS servicios_autentificacion
    CHARACTER SET = utf8
    COLLATE = utf8_general_ci;

USE servicios_autentificacion;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255),
    Correo VARCHAR(255),
    Pasword VARCHAR(255),
    Identificacion VARCHAR(255),
    Direccion VARCHAR(255),
    Rol INT(11)
) ENGINE=InnoDB;