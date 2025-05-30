-- 1) Eliminar la base de datos si existe y crearla nuevamente
DROP DATABASE IF EXISTS dbelektra;
CREATE DATABASE dbelektra;
USE dbelektra;

-- ---------------------------------------------------------
-- 2) Tabla: Categoria (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------
-- 3) Tabla: Unidad (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Unidad (
    id_unidad INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------
-- 4) Tabla: Proveedor (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Proveedor (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono CHAR(10),
    representante VARCHAR(50)
);

-- ---------------------------------------------------------
-- 5) Tabla: Cliente (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Cliente (
    telefono CHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(255),
    rfc CHAR(13)
);

-- ---------------------------------------------------------
-- 6) Tabla: Usuarios (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    departamento VARCHAR(50),
    salario INT,
    telefono CHAR(10),
    contraseña VARCHAR(20) NOT NULL
);

-- ---------------------------------------------------------
-- 7) Tabla: Articulo (MODIFICADA - código como VARCHAR)
-- ---------------------------------------------------------
CREATE TABLE Articulo (
    codigo VARCHAR(13) PRIMARY KEY,  -- Cambiado de INT a VARCHAR(13)
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
-- 8) Tabla: Venta (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Venta (
    id_venta INT PRIMARY KEY,
    fecha DATE NOT NULL,
    importe DECIMAL(10, 2) NOT NULL,
    telefono CHAR(10) NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (telefono) REFERENCES Cliente(telefono),
    CONSTRAINT fk_venta_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- ---------------------------------------------------------
-- 9) Tabla: DetalleVenta (MODIFICADA - código como VARCHAR)
-- ---------------------------------------------------------
CREATE TABLE DetalleVenta (
    id_venta INT,
    codigo VARCHAR(13) NOT NULL,  -- Cambiado de INT a VARCHAR(13)
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_venta, codigo),
    CONSTRAINT fk_detalleventa_venta
        FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
    CONSTRAINT fk_detalleventa_articulo
        FOREIGN KEY (codigo) REFERENCES Articulo(codigo)
);

-- ---------------------------------------------------------
-- 10) Tabla: Compra (sin cambios)
-- ---------------------------------------------------------
CREATE TABLE Compra (
    id_compra INT PRIMARY KEY,
    numdoc VARCHAR(50) NOT NULL,
    tipodoc VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    importe DECIMAL(10, 2) NOT NULL,
    id_proveedor INT NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_compra_proveedor
        FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
    CONSTRAINT fk_compra_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- ---------------------------------------------------------
-- 11) Tabla: DetalleCompra (MODIFICADA - código como VARCHAR)
-- ---------------------------------------------------------
CREATE TABLE DetalleCompra (
    id_compra INT,
    codigo VARCHAR(13) NOT NULL,  -- Cambiado de INT a VARCHAR(13)
    cantidad INT NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_compra, codigo),
    CONSTRAINT fk_detallecompra_compra
        FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
    CONSTRAINT fk_detallecompra_articulo
        FOREIGN KEY (codigo) REFERENCES Articulo(codigo)
);


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
    (16, 'Papelería y Oficina');

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

INSERT INTO Proveedor (id_proveedor, nombre, telefono, representante) VALUES
  (11, 'Oster México',                '9611000021', 'Julio Ramírez'),
  (12, 'Midea México',                '9611000022', 'Ana Castillo'),
  (13, 'Winia México',                '9611000023', 'Sara López'),
  (14, 'Misik Audio',                 '9611000024', 'Diego Martínez'),
  (15, 'Truper México',               '9611000025', 'Carlos Vega');

    -- ---------------------------------------------------------
-- Extensión: Usuarios
-- ---------------------------------------------------------
INSERT INTO Usuarios (id_usuario, nombre, departamento, salario, telefono, contraseña) VALUES 
(1, 'Administrador', 'Administrador', 10000, '9161579322', '07'),
(2, 'Vendedor General', 'Ventas', 0, '9161579322', 'elektra');

    -- ---------------------------------------------------------
-- Extensión: Clientes
-- ---------------------------------------------------------
INSERT INTO Cliente (telefono, nombre, direccion, rfc) VALUES 
('5512345678', 'Rodrigo Gonzalez', 'Calle 10 #123, Ciudad X', 'ABC123456XYZ'),
('5523456789', 'Alejandro Gutierrez', 'Av. Central #456, Ciudad Y', 'ALF456789DEF'),
('5534567890', 'Kaleb Toledo', 'Boulevard Norte #789, Ciudad Z', 'SER789012GHI'),
('0000000000', 'Venta General',NULL,NULL);

-- 2) Insertar los artículos (manteniendo código y nombre)
INSERT INTO Articulo (
  codigo, nombre, precio, costo, existencia, reorden,
  id_categoria, id_proveedor, id_unidad
) VALUES
  -- Lavadora Mabe 16 Kg Blanca
  ("757638969444", 'Lavadora Mabe 16 Kg Blanca',
    12999.00, 10500.00, 15, 5,
    6,   -- Línea Blanca
    6,   -- Mabe de México
    1),  -- Pieza

  -- Licuadora Oster ActiveSense roja
  ("7501095200908", 'Licuadora Oster ActiveSense roja',
     899.00,   650.00, 30, 10,
     1,   -- Electrodomésticos
    11,   -- Oster México
     1),  -- Pieza

  -- Minisplit Midea 1.5 Toneladas 220v Frío
  ("6938187347394", 'Minisplit Midea 1.5 Toneladas 220v Frio',
  11999.00,  9000.00, 10, 3,
     1,   -- Electrodomésticos
    12,   -- Midea México
     1),  -- Pieza

  -- Horno de microondas Winia KOS-81HS
  ("7501744619891", 'Horno de microondas Winia KOS-81HS',
   2399.00, 1800.00, 20, 5,
     1,   -- Electrodomésticos
    13,   -- Winia México
     1),  -- Pieza

  -- Audífonos inalambricos Misik MH624 negro
  ("089081900508", 'Audifonos inalambricos Misik MH624 negro',
   1299.00,   800.00, 25, 5,
     5,   -- Audio y Video
    14,   -- Misik Audio
     1),  -- Pieza

  -- Truper Maletín Suave Portaherramienta 22
  ("7506240607762", 'Truper Maletín Suave Portaherramienta 22',
     799.00,   600.00, 40, 10,
     9,   -- Herramientas y Ferretería
    15,   -- Truper México
     1);  -- Pieza


-- Extension de mas articulos de elektra 

INSERT INTO Articulo (
  codigo, nombre, precio, costo, existencia, reorden,
  id_categoria, id_proveedor, id_unidad
) VALUES
  ("7501031312345", 'Refrigerador Samsung RT29K571JS8', 17999.00, 14500.00, 10, 3, 6, 1, 1),
  ("7501293305678", 'Pantalla LG Smart TV 50" UHD 4K', 11499.00, 9000.00, 12, 4, 2, 2, 1),
  ("7501094201111", 'iPhone 14 128GB Medianoche', 18999.00, 16000.00, 8, 2, 3, 3, 1),
  ("7501022908765", 'Laptop HP Pavilion 15.6" Ryzen 7', 15499.00, 12500.00, 6, 2, 4, 4, 1),
  ("7501032237896", 'Barra de Sonido Sony HT-S400 2.1', 4499.00, 3600.00, 10, 2, 5, 5, 1),
  ("7501021144221", 'Cama Matrimonial Dico Venice Café', 9999.00, 7800.00, 5, 1, 7, 9, 1),
  ("7501025567834", 'Escritorio Oficina Roble Oscuro', 2899.00, 2100.00, 15, 3, 8, 10, 1),
  ("7501055554321", 'Cortadora Truper Industrial 14"', 3199.00, 2550.00, 7, 2, 9, 15, 1),
  ("7501002223456", 'Tenis Nike Air Max 270 Hombre', 2999.00, 2200.00, 20, 5, 11, 8, 11),
  ("7501098765432", 'Set Belleza Conair Secadora + Plancha', 1599.00, 1200.00, 18, 4, 12, 5, 10);
