CREATE TABLE `urllist` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `status` int(2) DEFAULT '0',
  `type` enum('央媒','央企','地方','部委','商网','app') DEFAULT '商网',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1155 DEFAULT CHARSET=utf8 COMMENT='进行灰度检测的URL分为APP和Web';


CREATE TABLE `v6view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(56) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  `prov` varchar(32) DEFAULT NULL,
  `city` varchar(32) DEFAULT NULL,
  `ipv4` varchar(64) DEFAULT NULL,
  `ipv6` varchar(64) DEFAULT NULL,
  `ipv4stat` varchar(8) DEFAULT NULL,
  `ipv6stat` varchar(8) DEFAULT NULL,
  `httpstat` varchar(8) DEFAULT NULL,
  `regstat` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=937 DEFAULT CHARSET=utf8 COMMENT='所有节点的列表，需要定时从网站下载更新';

CREATE TABLE `webprobe2` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `nodename` varchar(64) DEFAULT NULL,
  `website` varchar(64) DEFAULT NULL,
  `code` varchar(8) DEFAULT NULL,
  `ipv6addr` blob,
  `ipv4addr` blob,
  `acsrate` float(8,2) DEFAULT NULL,
  `acsdelay` float(8,2) DEFAULT NULL,
  `ipver` enum('6','4') DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `md5hash` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index` (`md5hash`)
) ENGINE=InnoDB AUTO_INCREMENT=59006 DEFAULT CHARSET=utf8 COMMENT='是对网站进行灰度检测的结果';

CREATE TABLE `webresp` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `idx` varchar(8) DEFAULT NULL,
  `result` varchar(128) DEFAULT NULL,
  `status` int(2) DEFAULT '0',
  `ipver` enum('6','4') DEFAULT NULL,
  `md5hash` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index` (`md5hash`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=26697 DEFAULT CHARSET=utf8;


CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `active` AS select `v6view`.`id` AS `id`,`v6view`.`name` AS `name`,`v6view`.`type` AS `type`,`v6view`.`prov` AS `prov`,`v6view`.`city` AS `city`,`v6view`.`ipv4` AS `ipv4`,`v6view`.`ipv6` AS `ipv6`,`v6view`.`ipv4stat` AS `ipv4stat`,`v6view`.`ipv6stat` AS `ipv6stat`,`v6view`.`httpstat` AS `httpstat`,`v6view`.`regstat` AS `regstat` from `v6view` where ((`v6view`.`httpstat` = '200') and (`v6view`.`name` like '中国%'))


CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `1main_node` AS select distinct `active`.`type` AS `type`,`active`.`prov` AS `prov` from `active`

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `2main_node` AS select distinct `1main_node`.`type` AS `type`,`1main_node`.`prov` AS `prov`,(select `active`.`name` from `active` where ((`active`.`type` = `1main_node`.`type`) and (`active`.`prov` = `1main_node`.`prov`)) limit 1) AS `name` from (`active` join `1main_node`)

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `2main_node_2` AS select `active`.`id` AS `id`,`active`.`name` AS `name`,`active`.`type` AS `type`,`active`.`prov` AS `prov`,`active`.`city` AS `city`,`active`.`ipv4` AS `ipv4`,`active`.`ipv6` AS `ipv6`,`active`.`ipv4stat` AS `ipv4stat`,`active`.`ipv6stat` AS `ipv6stat`,`active`.`httpstat` AS `httpstat`,`active`.`regstat` AS `regstat` from `active` where (not(`active`.`name` in (select `2main_node`.`name` from `2main_node`)))


CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `2main_node_3` AS select distinct `1main_node`.`type` AS `type`,`1main_node`.`prov` AS `prov`,(select `2main_node_2`.`name` from `2main_node_2` where ((`2main_node_2`.`type` = `1main_node`.`type`) and (`2main_node_2`.`prov` = `1main_node`.`prov`)) limit 1) AS `name` from (`2main_node_2` join `1main_node`)

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `3main_node` AS select `active`.`id` AS `id`,`active`.`name` AS `name`,`active`.`type` AS `type`,`active`.`prov` AS `prov`,`active`.`city` AS `city`,`active`.`ipv4` AS `ipv4`,`active`.`ipv6` AS `ipv6`,`active`.`ipv4stat` AS `ipv4stat`,`active`.`ipv6stat` AS `ipv6stat`,`active`.`httpstat` AS `httpstat`,`active`.`regstat` AS `regstat` from (`active` join `2main_node`) where (`active`.`name` = `2main_node`.`name`)

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `webprobe_result2` AS select `webprobe2`.`id` AS `id`,`active`.`ipv4` AS `nodeaddr`,`urllist`.`name` AS `name`,cast(`webprobe2`.`ipv6addr` as char charset utf8) AS `ipv6`,cast(`webprobe2`.`ipv4addr` as char charset utf8) AS `ipv4`,`webprobe2`.`nodename` AS `nodename`,`webprobe2`.`website` AS `website`,`webprobe2`.`code` AS `code`,`webprobe2`.`acsrate` AS `acsrate`,`webprobe2`.`acsdelay` AS `acsdelay`,`webprobe2`.`ipver` AS `ipver`,`webprobe2`.`date` AS `date`,`webprobe2`.`md5hash` AS `md5hash` from ((`urllist` join `active`) join `webprobe2`) where ((`webprobe2`.`nodename` = `active`.`name`) and (`webprobe2`.`website` = `urllist`.`url`))
