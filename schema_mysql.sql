-- MySQL 8 schema for the DBMS demonstration.
CREATE DATABASE IF NOT EXISTS deadlock_system;
USE deadlock_system;

CREATE TABLE IF NOT EXISTS Processes (
  process_id INT AUTO_INCREMENT PRIMARY KEY,
  process_name VARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS Resources (
  resource_id INT AUTO_INCREMENT PRIMARY KEY,
  resource_name VARCHAR(20) NOT NULL UNIQUE,
  total_units INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS Resource_Allocation (
  allocation_id INT AUTO_INCREMENT PRIMARY KEY,
  process_id INT NOT NULL,
  resource_id INT NOT NULL,
  allocated_units INT NOT NULL DEFAULT 0,
  max_demand INT NOT NULL DEFAULT 0,
  CHECK (allocated_units >= 0),
  CHECK (max_demand >= allocated_units),
  FOREIGN KEY (process_id) REFERENCES Processes(process_id),
  FOREIGN KEY (resource_id) REFERENCES Resources(resource_id),
  UNIQUE KEY unique_process_resource (process_id, resource_id)
);
CREATE TABLE IF NOT EXISTS Analysis_Logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  algorithm_name VARCHAR(80) NOT NULL,
  is_safe BOOLEAN NOT NULL,
  safe_sequence VARCHAR(255) NOT NULL,
  available_vector JSON NOT NULL,
  message VARCHAR(255) NOT NULL
);
INSERT IGNORE INTO Processes(process_name) VALUES ('P1'),('P2'),('P3'),('P4'),('P5');
INSERT IGNORE INTO Resources(resource_name,total_units) VALUES ('R1',10),('R2',5),('R3',7);
