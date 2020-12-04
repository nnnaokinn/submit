CREATE TABLE IF NOT EXISTS youtube.channel (
  `channel_id` varchar(64) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `published_date` datetime DEFAULT NULL,
  `description` varchar(4096) DEFAULT NULL,
  `keyword` varchar(2048) DEFAULT NULL,
  `thumbnail_s` varchar(256) DEFAULT NULL,
  `thumbnail_m` varchar(256) DEFAULT NULL,
  `thumbnail_l` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS youtube.statistics (
  `collect_day` int NOT NULL,
  `channel_id` varchar(64) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `subscriber` int DEFAULT NULL,
  `video_count` int DEFAULT NULL,
  `view_count` bigint DEFAULT NULL,
  PRIMARY KEY (`collect_day`,`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

