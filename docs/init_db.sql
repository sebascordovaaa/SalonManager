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
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50),
    telefono VARCHAR(20)
);



CREATE TABLE servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);


CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    id_servicio INT NOT NULL,
    fecha DATETIME NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
);


INSERT INTO clientes (nombre, telefono, email)
VALUES ('Juan Pérez', '123456789', 'juan@mail.com');

INSERT INTO empleados (nombre, especialidad, telefono)
VALUES ('María López', 'Cortes', '987654321');

INSERT INTO servicios (nombre, precio)
VALUES ('Corte de cabello', 15.00);

INSERT INTO citas (id_cliente, id_empleado, id_servicio, fecha)
VALUES (1, 1, 1, '2026-01-20 15:00:00');
