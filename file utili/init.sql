-- Adminer 4.8.1 MySQL 8.0.40 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `foodies_db`;
CREATE DATABASE `foodies_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `foodies_db`;

DROP TABLE IF EXISTS `Ordini`;
CREATE TABLE `Ordini` (
  `order_id` varchar(5) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `status` enum('PENDING','CONFIRMED','FAILED') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `amount` decimal(10,2) DEFAULT NULL,
  `meal` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Ordini` (`order_id`, `username`, `status`, `created_at`, `updated_at`, `amount`, `meal`) VALUES
('86326',	'user',	'CONFIRMED',	'2024-12-09 15:15:05',	'2024-12-09 15:15:05',	36.00,	'hot roll');

DROP TABLE IF EXISTS `Pagamenti`;
CREATE TABLE `Pagamenti` (
  `payment_id` varchar(5) NOT NULL,
  `order_id` varchar(5) NOT NULL,
  `username` varchar(255) NOT NULL,
  `payment_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `amount` decimal(10,2) NOT NULL,
  `status` enum('SUCCESS','FAILED') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Pagamenti` (`payment_id`, `order_id`, `username`, `payment_timestamp`, `amount`, `status`) VALUES
('33377',	'86326',	'user',	'2024-12-09 15:15:05',	36.00,	'SUCCESS');

DROP TABLE IF EXISTS `Utenti`;
CREATE TABLE `Utenti` (
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(60) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `admin` int NOT NULL,
  `credito` decimal(10,2) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `Utenti` (`username`, `password`, `email`, `admin`, `credito`) VALUES
('admin',	'$2b$12$cmqAR4MH0k4dB8fInx1i3uI/Cx6GBo8Pv0F.FTHFzr2GoYikmDJHO',	'admin@foodies.com',	1,	0.00),
('user',	'$2b$12$3kW9ABGJDeZJa9wb9okBbug/pcD3Gh2d.RIO2.0ZJvkJskjUkdGEi',	'user@foodies.com',	0,	364.00);

-- 2024-12-09 15:15:37
