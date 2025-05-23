-- ---------------------------------------------------------
-- 1) Crear la base de datos y seleccionarla
-- ---------------------------------------------------------
CREATE DATABASE db23270653;
USE db23270653;

-- ---------------------------------------------------------
-- 2) Tabla: Categoria
-- ---------------------------------------------------------
CREATE TABLE Categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------
-- 3) Tabla: Unidad
-- ---------------------------------------------------------
CREATE TABLE Unidad (
    id_unidad INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------
-- 4) Tabla: Proveedor
-- ---------------------------------------------------------
CREATE TABLE Proveedor (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono CHAR(10),
    representante VARCHAR(50)   -- Se cambió 'contacto' por 'representante'
);

-- ---------------------------------------------------------
-- 5) Tabla: Cliente
-- ---------------------------------------------------------
CREATE TABLE Cliente (
    telefono CHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(255),
    rfc CHAR(13)
);


-- ---------------------------------------------------------
-- 11) Tabla: Usuarios (antes Empleado)
-- ---------------------------------------------------------
CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY,            -- Antes era id_empleado
    nombre VARCHAR(50) NOT NULL,
    departamento VARCHAR(50),
    salario INT,
    telefono CHAR(10),
    contraseña VARCHAR(20) NOT NULL       -- Nueva columna añadida
);

-- ---------------------------------------------------------
-- 6) Tabla: Articulo
-- ---------------------------------------------------------
CREATE TABLE Articulo (
    codigo INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    existencia INT NOT NULL,
    reorden INT NOT NULL,
    id_categoria INT NOT NULL,
    id_proveedor INT NOT NULL,
    id_unidad INT NOT NULL,
    CONSTRAINT fk_articulo_categoria 
        FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
    CONSTRAINT fk_articulo_proveedor 
        FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
    CONSTRAINT fk_articulo_unidad
        FOREIGN KEY (id_unidad) REFERENCES Unidad(id_unidad)
);

-- ---------------------------------------------------------
-- 7) Tabla: Venta
-- ---------------------------------------------------------
CREATE TABLE Venta (
    id_venta INT PRIMARY KEY,
    fecha DATE NOT NULL,
    importe DECIMAL(10, 2) NOT NULL,
    telefono CHAR(10) NOT NULL,
    id_usuario INT NOT NULL,    -- Se cambió de id_empleado a id_usuario
    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (telefono) REFERENCES Cliente(telefono),
    CONSTRAINT fk_venta_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- ---------------------------------------------------------
-- 8) Tabla: DetalleVenta
-- ---------------------------------------------------------
CREATE TABLE DetalleVenta (
    id_venta INT,
    codigo INT,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_venta, codigo),
    CONSTRAINT fk_detalleventa_venta
        FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
    CONSTRAINT fk_detalleventa_articulo
        FOREIGN KEY (codigo) REFERENCES Articulo(codigo)
);

-- ---------------------------------------------------------
-- 9) Tabla: Compra
-- ---------------------------------------------------------
CREATE TABLE Compra (
    id_compra INT PRIMARY KEY,
    numdoc VARCHAR(50) NOT NULL,
    tipodoc VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    importe DECIMAL(10, 2) NOT NULL,
    id_proveedor INT NOT NULL,
    id_usuario INT NOT NULL,    -- Se cambió de id_empleado a id_usuario
    CONSTRAINT fk_compra_proveedor
        FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
    CONSTRAINT fk_compra_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- ---------------------------------------------------------
-- 10) Tabla: DetalleCompra
-- ---------------------------------------------------------
CREATE TABLE DetalleCompra (
    id_compra INT,
    codigo INT,
    cantidad INT NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_compra, codigo),
    CONSTRAINT fk_detallecompra_compra
        FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
    CONSTRAINT fk_detallecompra_articulo
        FOREIGN KEY (codigo) REFERENCES Articulo(codigo)
);



-- Script para eliminar los campos de hora de entrada y salida


-- Mostrar las tablas creadas
SHOW TABLES;



-- ---------------------------------------------------------
-- Extensión: Insertar categorías predeterminadas para Elektra
-- ---------------------------------------------------------
INSERT INTO Categoria (id_categoria, nombre) VALUES
    (1,  'Electrodomésticos'),
    (2,  'Electrónica'),
    (3,  'Celulares y Smartphones'),
    (4,  'Computación'),
    (5,  'Audio y Video'),
    (6,  'Línea Blanca'),
    (7,  'Muebles'),
    (8,  'Hogar y Decoración'),
    (9,  'Herramientas y Ferretería'),
    (10, 'Juguetes'),
    (11, 'Ropa y Calzado'),
    (12, 'Belleza y Cuidado Personal'),
    (13, 'Deportes y Fitness'),
    (14, 'Alimentos y Bebidas'),
    (15, 'Automotriz'),
    (16, 'Papelería y Oficina'),
    (17, 'Salud y Medicinas');

-- ---------------------------------------------------------
-- Extensión: Insertar unidades de medida predeterminadas para Elektra
-- ---------------------------------------------------------
INSERT INTO Unidad (id_unidad, nombre) VALUES
    (1,  'Pieza'),
    (2,  'Caja'),
    (3,  'Kilogramo'),
    (4,  'Gramo'),
    (5,  'Litro'),
    (6,  'Mililitro'),
    (7,  'Metro'),
    (8,  'Centímetro'),
    (9,  'Paquete'),
    (10, 'Set'),
    (11, 'Par'),
    (12, 'Botella'),
    (13, 'Unidad'),
    (14, 'Rollos'),
    (15, 'Tira');
    
    -- ---------------------------------------------------------
-- Extensión: Proveedores reales con lada 961 (Chiapas)
-- ---------------------------------------------------------
INSERT INTO Proveedor (id_proveedor, nombre, telefono, representante) VALUES
    (1,  'Samsung Electronics Mexico',    '9611000001', 'Luis Herrera'),
    (2,  'LG Electronics Mexico',         '9611000002', 'Laura Méndez'),
    (3,  'Apple de México',               '9611000003', 'Carlos Jiménez'),
    (4,  'HP México',                     '9611000004', 'María Torres'),
    (5,  'Sony de México',                '9611000005', 'Ricardo Gómez'),
    (6,  'Mabe de México',                '9611000007', 'Pedro Sánchez'),
    (7,  'Office Depot México',           '9611000008', 'Verónica Castillo'),
    (8, 'Nike México',                   '9611000012', 'Paola Hernández'),
    (9, 'Muebles Dico',                  '9611000014', 'Ernesto López'),
    (10, 'Lamosa Hogar y Decoración',     '9611000015', 'Claudia Vargas');




    -- ---------------------------------------------------------
-- Extensión: Usuarios
-- ---------------------------------------------------------
INSERT INTO Usuarios (id_usuario, nombre, departamento, salario, telefono, contraseña) VALUES 
(1, 'Administrador', 'Administrador', 10000, '9161579322', '07');


    -- ---------------------------------------------------------
-- Extensión: Clientes
-- ---------------------------------------------------------
INSERT INTO Cliente (telefono, nombre, direccion, rfc) VALUES 
('5512345678', 'Rodrigo Gonzalez', 'Calle 10 #123, Ciudad X', 'ABC123456XYZ'),
('5523456789', 'Alejandro Gutierrez', 'Av. Central #456, Ciudad Y', 'ALF456789DEF'),
('5534567890', 'Kaleb Gopar', 'Boulevard Norte #789, Ciudad Z', 'SER789012GHI');

