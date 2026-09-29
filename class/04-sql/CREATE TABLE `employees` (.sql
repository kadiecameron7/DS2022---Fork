CREATE TABLE `employees` (
  `employee_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `state_id` int DEFAULT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci