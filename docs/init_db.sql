-- =========================================================
-- scipt basico para inicializar la base de datos
-- =========================================================

CREATE DATABASE peluqueria_db;
USE peluqueria_db;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(50),
    direccion VARCHAR(100),
    ciudad VARCHAR(50),
    estado VARCHAR(50),
    codigo_postal VARCHAR(10),
    fecha_nacimiento DATE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO clientes (nombre, telefono, email, direccion, ciudad, estado, codigo_postal, fecha_nacimiento) 
VALUES (
    'María López','555-123-4567', 'maria.lopez@email.com',  
    'Av. Reforma 123, Col. Centro', 'Ciudad de México', 'CDMX', '06000', '1985-04-15' );
