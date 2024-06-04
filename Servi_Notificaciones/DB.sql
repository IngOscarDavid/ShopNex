CREATE DATABASE IF NOT EXISTS servicios_notificaciones
    CHARACTER SET = 'utf8'
    COLLATE = 'utf8_general_ci';

USE servicios_notificaciones;

CREATE TABLE IF NOT EXISTS notificaiones(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Codigo_Usuario  VARCHAR(50),
    Texto VARCHAR(255),
    Estado VARCHAR(255)
) ENGINE=InnoDB;