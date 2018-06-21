/*
SQLyog v10.2 
MySQL - 5.7.18-log : Database - ipricejot
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`ipricejot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;

USE `ipricejot`;

/*Table structure for table `py_review_detail` */

DROP TABLE IF EXISTS `py_review_detail`;

CREATE TABLE `py_review_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `asin` varchar(11) CHARACTER SET utf8 NOT NULL COMMENT 'asin号',
  `review_id` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '评论id号',
  `reviewer` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '评论者',
  `review_url` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '评价链接',
  `star` varchar(4) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT '评论星级',
  `date` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '评论日期',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '评论标题',
  `content` text CHARACTER SET utf8 COMMENT '评论内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `asin_review_id_unique` (`asin`,`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2706 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Table structure for table `py_review_profile` */

DROP TABLE IF EXISTS `py_review_profile`;

CREATE TABLE `py_review_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `asin` varchar(11) NOT NULL COMMENT 'asin号',
  `product` varchar(500) NOT NULL COMMENT '产品名',
  `brand` varchar(255) NOT NULL COMMENT '商品标签',
  `seller` varchar(255) DEFAULT NULL COMMENT '销售商家',
  `image` varchar(255) NOT NULL DEFAULT '' COMMENT '图片地址',
  `review_total` int(11) NOT NULL DEFAULT '0' COMMENT '评论总数',
  `review_rate` varchar(4) NOT NULL DEFAULT '0' COMMENT '评论平均分值',
  `pct_five` tinyint(2) NOT NULL DEFAULT '0' COMMENT '5星所占比分比',
  `pct_four` tinyint(2) NOT NULL DEFAULT '0' COMMENT '4星所占百分比',
  `pct_three` tinyint(2) NOT NULL DEFAULT '0' COMMENT '3星所占百分比',
  `pct_two` tinyint(2) NOT NULL DEFAULT '0' COMMENT '2星所占百分比',
  `pct_one` tinyint(2) NOT NULL DEFAULT '0' COMMENT '1星所占百分比',
  `latest_total` int(11) DEFAULT NULL COMMENT '上一次的评论总数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_asin` (`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

/*Table structure for table `py_salesranking_keywords` */

DROP TABLE IF EXISTS `py_salesranking_keywords`;

CREATE TABLE `py_salesranking_keywords` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `skwd_id` int(11) NOT NULL COMMENT 'salesranking_keyword_id',
  `rank` int(11) NOT NULL COMMENT '排名',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '爬取时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `py_salesrankings` */

DROP TABLE IF EXISTS `py_salesrankings`;

CREATE TABLE `py_salesrankings` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sk_id` int(11) NOT NULL COMMENT 'salesranking_id',
  `rank` int(11) NOT NULL COMMENT '排名',
  `classify` varchar(150) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '分类',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '爬取时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `salesranking_keywords` */

DROP TABLE IF EXISTS `salesranking_keywords`;

CREATE TABLE `salesranking_keywords` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sk_id` int(11) NOT NULL COMMENT 'saleranking_id',
  `keyword` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '关键字',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '抓取状态 0抓取中 1成功 2抓取失败',
  `rank` int(11) NOT NULL DEFAULT '0' COMMENT '当前排名',
  `last_rank` int(11) NOT NULL DEFAULT '0' COMMENT '上次排名',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `salesranking_keywords_sk_id_keyword_unique` (`sk_id`,`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `salesrankings` */

DROP TABLE IF EXISTS `salesrankings`;

CREATE TABLE `salesrankings` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(11) NOT NULL COMMENT 'seller_uid',
  `asin` varchar(11) COLLATE utf8_unicode_ci NOT NULL COMMENT '商品asin号',
  `title` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '商品名称',
  `image` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '商品图片',
  `link` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '亚马逊商品链接',
  `classify` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品分类',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '抓取状态 0抓取中 1成功 2抓取失败',
  `rank` int(11) NOT NULL DEFAULT '0' COMMENT '目前排名',
  `last_rank` int(11) NOT NULL DEFAULT '0' COMMENT '上次排名',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `salesrankings_sid_asin_unique` (`sid`,`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
