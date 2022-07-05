-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.4.21-MariaDB - Source distribution
-- Операционная система:         Linux
-- HeidiSQL Версия:              12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Дамп структуры базы данных phototur
CREATE DATABASE IF NOT EXISTS `phototur` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `phototur`;

-- Дамп структуры для таблица phototur.blog
CREATE TABLE IF NOT EXISTS `blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL DEFAULT 0,
  `short_text` varchar(136) NOT NULL,
  `long_text` text NOT NULL,
  `pic` varchar(256) NOT NULL DEFAULT '',
  `showed` tinyint(4) NOT NULL DEFAULT 0,
  `lastdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_USER` (`id_user`),
  CONSTRAINT `FK_USER` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.blog: ~0 rows (приблизительно)

-- Дамп структуры для таблица phototur.contacts
CREATE TABLE IF NOT EXISTS `contacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vk` varchar(128) NOT NULL,
  `instagram` varchar(128) NOT NULL,
  `telegram` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  `phone` varchar(128) NOT NULL,
  `desc` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.contacts: ~0 rows (приблизительно)

-- Дамп структуры для таблица phototur.heads
CREATE TABLE IF NOT EXISTS `heads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `type_head` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_head` (`type_head`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.heads: ~0 rows (приблизительно)

-- Дамп структуры для таблица phototur.staffs
CREATE TABLE IF NOT EXISTS `staffs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `vk` varchar(128) DEFAULT NULL,
  `instagram` varchar(128) DEFAULT NULL,
  `telegram` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.staffs: ~0 rows (приблизительно)

-- Дамп структуры для таблица phototur.stories
CREATE TABLE IF NOT EXISTS `stories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(255) NOT NULL,
  `pic` varchar(256) NOT NULL,
  `bg_text` varchar(20) DEFAULT NULL,
  `up_head` varchar(20) DEFAULT NULL,
  `down_head` varchar(20) DEFAULT NULL,
  `type_stories` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_stories` (`type_stories`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.stories: ~0 rows (приблизительно)

-- Дамп структуры для таблица phototur.system
CREATE TABLE IF NOT EXISTS `system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) DEFAULT NULL,
  `icon` varchar(256) DEFAULT NULL,
  `bg_pic` varchar(256) DEFAULT NULL,
  `main_video` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.system: ~0 rows (приблизительно)
INSERT INTO `system` (`id`, `title`, `icon`, `bg_pic`, `main_video`) VALUES
	(1, 'title1', 'icon', 'bg', 'video');

-- Дамп структуры для таблица phototur.trips
CREATE TABLE IF NOT EXISTS `trips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `price` int(11) NOT NULL DEFAULT 0,
  `short_desc` varchar(33) NOT NULL,
  `description` text NOT NULL,
  `photo_list` text NOT NULL,
  `showed` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.trips: ~2 rows (приблизительно)
INSERT INTO `trips` (`id`, `name`, `price`, `short_desc`, `description`, `photo_list`, `showed`) VALUES
	(1, '1', 2, '3', '4', '5', 0),
	(2, '1', 2, '3', '4', '5', 1);

-- Дамп структуры для таблица phototur.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `is_admin` tinyint(4) DEFAULT 0,
  `is_delete` tinyint(4) DEFAULT 0,
  `lastdate` timestamp NULL DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `about` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы phototur.users: ~1 rows (приблизительно)
INSERT INTO `users` (`id`, `login`, `name`, `is_admin`, `is_delete`, `lastdate`, `password_hash`, `about`) VALUES
	(1, 'root', NULL, 0, 0, '2022-06-08 19:48:12', 'pbkdf2:sha256:260000$O47qWC8cnXBBTWLG$39821956e7ae4a07b2c5be777ff84ae81e1ef386e235f250294f1b1349785509', '');

-- Дамп структуры для триггер phototur.BI_BLOG
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `BI_BLOG` BEFORE INSERT ON `blog` FOR EACH ROW BEGIN
	SET NEW.lastdate = CURRENT_TIMESTAMP();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Дамп структуры для триггер phototur.BU_BLOG
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `BU_BLOG` BEFORE UPDATE ON `blog` FOR EACH ROW BEGIN
	SET NEW.lastdate = CURRENT_TIMESTAMP();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
