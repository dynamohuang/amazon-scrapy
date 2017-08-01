SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `py_cates`
-- ----------------------------
DROP TABLE IF EXISTS `py_cates`;
CREATE TABLE `py_cates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(512) NOT NULL,
  `link` varchar(512) NOT NULL,
  `level` tinyint(2) NOT NULL DEFAULT '1',
  `pid` int(11) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `py_asin_best`
-- ----------------------------
DROP TABLE IF EXISTS `py_asin_best`;
CREATE TABLE `py_asin_best` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asin` char(10) NOT NULL,
  `cid` int(11) NOT NULL,
  `rank` tinyint(4) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
