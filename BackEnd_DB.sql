CREATE DATABASE monitor;
USE monitor;

CREATE TABLE connections_bandwidth (
  id INT PRIMARY KEY AUTO_INCREMENT,
  date TIMESTAMP NOT NULL,
  interface VARCHAR(50) NOT NULL,
  bytes_received INT NOT NULL,
  bytes_sent INT NOT NULL,
  download FLOAT(16, 4),
  upload FLOAT(16, 4),
  ping FLOAT(8, 4),
  server_id INT NOT NULL,
  ip VARCHAR(15) NOT NULL,
  lat FLOAT(8, 5),
  lon FLOAT(8, 5));

CREATE TABLE connections_servers (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  host VARCHAR(255) NOT NULL,
  lat FLOAT(8, 5),
  lon FLOAT(8, 5),
  latency FLOAT(8, 4)
);