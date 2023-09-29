DROP DATABASE IF EXISTS payvast;
GO

CREATE DATABASE Payvast;
GO

USE Payvast
GO


CREATE TABLE Warehouse (
  id INT IDENTITY(1,1) PRIMARY KEY,
  name varchar(255) NOT NULL,
)
GO

CREATE TABLE Product (
  id INT IDENTITY(1,1) PRIMARY KEY,
  name varchar(255) NOT NULL,
)
GO

CREATE TABLE ProductCount (
  id INT IDENTITY(1,1) PRIMARY KEY,
  product_id INT NOT NULL,
  ware_house_id INT NOT Null,
  amount INT NOT NULL
  UNIQUE(product_id, ware_house_id)
)
GO

CREATE TABLE Inventory (
  id INT IDENTITY(1,1) PRIMARY KEY,
  product_id INT NOT NULL,
  ware_house_id INT NOT NULL,
  delivery_person_id INT NOT NULL,
  receiver_person_id INT NOT NULL,
  kind BIT NOT NULL,
  quantity INT NOT NULL,
  created_at datetime DEFAULT GETDATE() NOT NULL
)
GO

CREATE TABLE Person (
  id INT IDENTITY(1,1) PRIMARY KEY,
  name varchar(255) NOT NULL,
  password varchar(255) NOT NULL
)
GO

ALTER TABLE Inventory ADD FOREIGN KEY (ware_house_id) REFERENCES Warehouse (id)
GO

ALTER TABLE Inventory ADD FOREIGN KEY (product_id) REFERENCES Product (id)
GO

ALTER TABLE Inventory ADD FOREIGN KEY (delivery_person_id) REFERENCES Person (id)
GO

ALTER TABLE Inventory ADD FOREIGN KEY (receiver_person_id) REFERENCES Person (id)
GO

ALTER TABLE ProductCount ADD FOREIGN KEY (ware_house_id) REFERENCES Warehouse (id)
GO

ALTER TABLE ProductCount ADD FOREIGN KEY (product_id) REFERENCES Product (id)
GO



CREATE TABLE Inventory (
    id INT PRIMARY KEY IDENTITY(1,1),
    product_id INT NOT NULL,
    ware_house_id INT NOT NULL,
    delivery_person_id INT NOT NULL,
    receiver_person_id INT NOT NULL,
    kind BIT NOT NULL,
    quantity INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (ware_house_id) REFERENCES Warehouse(id),
    FOREIGN KEY (delivery_person_id) REFERENCES Person(id),
    FOREIGN KEY (receiver_person_id) REFERENCES Person(id)
);

CREATE TABLE Person (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255)
);

CREATE TABLE ProductCount (
    id INT PRIMARY KEY IDENTITY(1,1),
    product_id INT NOT NULL,
    ware_house_id INT NOT NULL,
    amount INT NOT NULL,
    CONSTRAINT UC_ProductWarehouse UNIQUE (product_id, ware_house_id),
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (ware_house_id) REFERENCES Warehouse(id)
);

CREATE TABLE Product (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Warehouse (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL
);
