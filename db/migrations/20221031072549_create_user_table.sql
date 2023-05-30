-- migrate:up
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` datetime(6) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `email_index` ((json_value(`email`, _utf8mb4'$.data' returning char(255))))
);


-- migrate:down
