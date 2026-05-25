-- MySQL dump 10.13  Distrib 8.4.3, for Linux (aarch64)
--
-- Host: localhost    Database: travelSchema_v2
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Balance`
--

DROP TABLE IF EXISTS `Balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Balance` (
  `balanceId` int NOT NULL AUTO_INCREMENT,
  `tripId` varchar(6) NOT NULL,
  `userId` int NOT NULL,
  `expenseId` int NOT NULL,
  `amount` float NOT NULL,
  `borrowedFrom` int DEFAULT NULL,
  PRIMARY KEY (`balanceId`,`tripId`,`userId`,`expenseId`),
  KEY `tripId` (`tripId`),
  KEY `userId` (`userId`),
  KEY `expenseId` (`expenseId`),
  KEY `borrowedFrom` (`borrowedFrom`),
  CONSTRAINT `Balance_ibfk_1` FOREIGN KEY (`tripId`) REFERENCES `trips` (`tripIdShared`) ON DELETE CASCADE,
  CONSTRAINT `Balance_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  CONSTRAINT `Balance_ibfk_3` FOREIGN KEY (`expenseId`) REFERENCES `expenses` (`expenseId`) ON DELETE CASCADE,
  CONSTRAINT `Balance_ibfk_4` FOREIGN KEY (`borrowedFrom`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=683 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Balance`
--

LOCK TABLES `Balance` WRITE;
/*!40000 ALTER TABLE `Balance` DISABLE KEYS */;
INSERT INTO `Balance` VALUES (380,'ueQdUr',35,3,-3918.5,37),(381,'ueQdUr',37,3,3918.5,37),(382,'ueQdUr',35,4,-4994,37),(383,'ueQdUr',37,4,4994,37),(384,'ueQdUr',35,7,-6147,37),(385,'ueQdUr',37,7,6147,37),(386,'ueQdUr',37,8,-1123,35),(387,'ueQdUr',35,8,1123,35),(388,'ueQdUr',35,12,-532.5,37),(389,'ueQdUr',37,12,532.5,37),(390,'ueQdUr',35,13,-50,37),(391,'ueQdUr',37,13,50,37),(392,'ueQdUr',37,15,-57,35),(393,'ueQdUr',35,15,57,35),(394,'ueQdUr',35,16,-100,37),(395,'ueQdUr',37,16,100,37),(396,'ueQdUr',37,19,-360,35),(397,'ueQdUr',35,19,360,35),(398,'ueQdUr',37,20,-125,35),(399,'ueQdUr',35,20,125,35),(400,'ueQdUr',37,21,-80,35),(401,'ueQdUr',35,21,80,35),(402,'ueQdUr',37,22,-60,35),(403,'ueQdUr',35,22,60,35),(404,'ueQdUr',37,23,-150,35),(405,'ueQdUr',35,23,150,35),(406,'ueQdUr',37,24,-500,35),(407,'ueQdUr',35,24,500,35),(408,'ueQdUr',37,25,-120,35),(409,'ueQdUr',35,25,120,35),(410,'ueQdUr',37,26,-152,35),(411,'ueQdUr',35,26,152,35),(412,'ueQdUr',37,27,-63,35),(413,'ueQdUr',35,27,63,35),(414,'ueQdUr',37,28,-1164.5,35),(415,'ueQdUr',35,28,1164.5,35),(416,'ueQdUr',37,29,-75,35),(417,'ueQdUr',35,29,75,35),(418,'ueQdUr',37,30,-94.5,35),(419,'ueQdUr',35,30,94.5,35),(420,'ueQdUr',37,31,-191.5,35),(421,'ueQdUr',35,31,191.5,35),(422,'ueQdUr',37,32,-540,35),(423,'ueQdUr',35,32,540,35),(424,'ueQdUr',37,33,-67.5,35),(425,'ueQdUr',35,33,67.5,35),(426,'ueQdUr',37,34,-75,35),(427,'ueQdUr',35,34,75,35),(428,'ueQdUr',37,35,-147.5,35),(429,'ueQdUr',35,35,147.5,35),(430,'ueQdUr',37,36,-110,35),(431,'ueQdUr',35,36,110,35),(432,'ueQdUr',37,37,-300,35),(433,'ueQdUr',35,37,300,35),(434,'ueQdUr',37,43,-725,35),(435,'ueQdUr',35,43,725,35),(436,'ueQdUr',35,44,-25,37),(437,'ueQdUr',37,44,25,37),(438,'ueQdUr',35,46,-230,37),(439,'ueQdUr',37,46,230,37),(440,'ueQdUr',35,47,-230,37),(441,'ueQdUr',37,47,230,37),(442,'ueQdUr',35,48,-43,37),(443,'ueQdUr',37,48,43,37),(444,'ueQdUr',35,49,-45,37),(445,'ueQdUr',37,49,45,37),(446,'ueQdUr',35,50,-2536,37),(447,'ueQdUr',37,50,2536,37),(448,'ueQdUr',35,51,-150,37),(449,'ueQdUr',37,51,150,37),(450,'ueQdUr',35,52,-250,37),(451,'ueQdUr',37,52,250,37),(452,'ueQdUr',35,53,-75,37),(453,'ueQdUr',37,53,75,37),(454,'ueQdUr',35,54,-120,37),(455,'ueQdUr',37,54,120,37),(456,'ueQdUr',35,55,-115,37),(457,'ueQdUr',37,55,115,37),(458,'ueQdUr',35,58,-90,37),(459,'ueQdUr',37,58,90,37),(460,'bx7dc0',35,80,-2900,37),(461,'bx7dc0',37,80,2900,37),(462,'bx7dc0',35,81,-190,37),(463,'bx7dc0',37,81,190,37),(464,'bx7dc0',35,82,-731.5,37),(465,'bx7dc0',37,82,731.5,37),(466,'bx7dc0',35,83,-143,37),(467,'bx7dc0',37,83,143,37),(468,'bx7dc0',35,84,-512,37),(469,'bx7dc0',37,84,512,37),(470,'bx7dc0',35,85,-427.5,37),(471,'bx7dc0',37,85,427.5,37),(472,'bx7dc0',35,86,-250,37),(473,'bx7dc0',37,86,250,37),(474,'bx7dc0',37,87,-90,35),(475,'bx7dc0',35,87,90,35),(476,'bx7dc0',37,88,-444,35),(477,'bx7dc0',35,88,444,35),(478,'bx7dc0',37,89,-65.5,35),(479,'bx7dc0',35,89,65.5,35),(480,'bx7dc0',37,90,-362.5,35),(481,'bx7dc0',35,90,362.5,35),(482,'bx7dc0',37,91,-300,35),(483,'bx7dc0',35,91,300,35),(484,'bx7dc0',37,92,-723,35),(485,'bx7dc0',35,92,723,35),(486,'bx7dc0',37,93,-280,35),(487,'bx7dc0',35,93,280,35),(488,'bx7dc0',37,95,-225,35),(489,'bx7dc0',35,95,225,35),(490,'93XXiM',35,96,-3362,37),(491,'93XXiM',37,96,3362,37),(492,'93XXiM',37,97,-13315,35),(493,'93XXiM',35,97,13315,35),(494,'93XXiM',37,98,-1255.5,35),(495,'93XXiM',35,98,1255.5,35),(496,'93XXiM',35,107,-230,37),(497,'93XXiM',37,107,230,37),(498,'93XXiM',35,108,-546,37),(499,'93XXiM',37,108,546,37),(500,'93XXiM',35,109,-200,37),(501,'93XXiM',37,109,200,37),(502,'93XXiM',37,110,-388.85,35),(503,'93XXiM',35,110,388.85,35),(504,'93XXiM',37,111,-70,35),(505,'93XXiM',35,111,70,35),(506,'93XXiM',37,112,-129.6,35),(507,'93XXiM',35,112,129.6,35),(508,'93XXiM',37,113,-648.1,35),(509,'93XXiM',35,113,648.1,35),(510,'93XXiM',37,114,-106.3,35),(511,'93XXiM',35,114,106.3,35),(512,'93XXiM',37,115,-215.15,35),(513,'93XXiM',35,115,215.15,35),(514,'93XXiM',37,116,-324.05,35),(515,'93XXiM',35,116,324.05,35),(516,'93XXiM',37,117,-531.45,35),(517,'93XXiM',35,117,531.45,35),(518,'93XXiM',37,118,-128.3,35),(519,'93XXiM',35,118,128.3,35),(520,'93XXiM',37,119,-259.25,35),(521,'93XXiM',35,119,259.25,35),(522,'93XXiM',37,120,-518.45,35),(523,'93XXiM',35,120,518.45,35),(524,'93XXiM',37,121,-220.35,35),(525,'93XXiM',35,121,220.35,35),(526,'93XXiM',37,122,-466.6,35),(527,'93XXiM',35,122,466.6,35),(528,'93XXiM',37,123,-181.45,35),(529,'93XXiM',35,123,181.45,35),(530,'93XXiM',37,124,-42.75,35),(531,'93XXiM',35,124,42.75,35),(532,'93XXiM',37,125,-129.6,35),(533,'93XXiM',35,125,129.6,35),(534,'93XXiM',35,126,-16742.5,37),(535,'93XXiM',37,126,16742.5,37),(536,'93XXiM',37,127,-181.1,35),(537,'93XXiM',35,127,181.1,35),(538,'93XXiM',37,128,-51.75,35),(539,'93XXiM',35,128,51.75,35),(540,'93XXiM',37,129,-77.6,35),(541,'93XXiM',35,129,77.6,35),(542,'93XXiM',37,130,-102.2,35),(543,'93XXiM',35,130,102.2,35),(544,'93XXiM',37,131,-155.25,35),(545,'93XXiM',35,131,155.25,35),(546,'93XXiM',35,132,-912.5,37),(547,'93XXiM',37,132,912.5,37),(548,'93XXiM',35,133,-323.4,37),(549,'93XXiM',37,133,323.4,37),(550,'93XXiM',37,134,-1277.4,35),(551,'93XXiM',35,134,1277.4,35),(552,'93XXiM',37,135,-178.85,35),(553,'93XXiM',35,135,178.85,35),(554,'93XXiM',37,136,-638.7,35),(555,'93XXiM',35,136,638.7,35),(556,'93XXiM',37,137,-638.7,35),(557,'93XXiM',35,137,638.7,35),(558,'93XXiM',37,138,-321.9,35),(559,'93XXiM',35,138,321.9,35),(560,'93XXiM',37,139,-638.7,35),(561,'93XXiM',35,139,638.7,35),(562,'93XXiM',37,141,-153.3,35),(563,'93XXiM',35,141,153.3,35),(564,'93XXiM',37,142,-319.35,35),(565,'93XXiM',35,142,319.35,35),(566,'93XXiM',37,143,-509.65,35),(567,'93XXiM',35,143,509.65,35),(568,'93XXiM',37,144,-15.35,35),(569,'93XXiM',35,144,15.35,35),(570,'93XXiM',37,146,-95.8,35),(571,'93XXiM',35,146,95.8,35),(572,'93XXiM',37,147,-646.85,35),(573,'93XXiM',35,147,646.85,35),(574,'93XXiM',37,148,-90.7,35),(575,'93XXiM',35,148,90.7,35),(576,'93XXiM',37,149,-191.6,35),(577,'93XXiM',35,149,191.6,35),(578,'93XXiM',37,150,-412.6,35),(579,'93XXiM',35,150,412.6,35),(580,'93XXiM',37,152,-191.6,35),(581,'93XXiM',35,152,191.6,35),(582,'93XXiM',35,153,-281,37),(583,'93XXiM',37,153,281,37),(584,'93XXiM',37,154,-560.75,35),(585,'93XXiM',35,154,560.75,35),(586,'93XXiM',37,155,-217.15,35),(587,'93XXiM',35,155,217.15,35),(588,'93XXiM',35,156,-1416,37),(589,'93XXiM',37,156,1416,37),(590,'93XXiM',35,157,-200,37),(591,'93XXiM',37,157,200,37),(592,'93XXiM',35,158,-553,37),(593,'93XXiM',37,158,553,37),(594,'93XXiM',35,160,-3216.5,37),(595,'93XXiM',37,160,3216.5,37),(596,'93XXiM',35,161,-5266,37),(597,'93XXiM',37,161,5266,37),(598,'93XXiM',37,163,-5441.65,35),(599,'93XXiM',35,163,5441.65,35),(600,'93XXiM',37,165,-58.75,35),(601,'93XXiM',35,165,58.75,35),(602,'93XXiM',37,166,-51.1,35),(603,'93XXiM',35,166,51.1,35),(604,'93XXiM',37,167,-127.75,35),(605,'93XXiM',35,167,127.75,35),(606,'93XXiM',37,168,-177.55,35),(607,'93XXiM',35,168,177.55,35),(608,'93XXiM',37,169,-2043.8,35),(609,'93XXiM',35,169,2043.8,35),(610,'93XXiM',37,170,-550,35),(611,'93XXiM',35,170,550,35),(612,'93XXiM',35,171,-750,37),(613,'93XXiM',37,171,750,37),(614,'93XXiM',37,172,-168,35),(615,'93XXiM',35,172,168,35),(616,'93XXiM',37,173,-187.5,35),(617,'93XXiM',35,173,187.5,35),(618,'93XXiM',37,174,-225.5,35),(619,'93XXiM',35,174,225.5,35),(620,'93XXiM',35,175,-350,37),(621,'93XXiM',37,175,350,37),(622,'93XXiM',37,176,-980.25,35),(623,'93XXiM',35,176,980.25,35),(624,'93XXiM',37,177,-328.05,35),(625,'93XXiM',35,177,328.05,35),(628,'bOQSFl',44,182,-1125,35),(629,'bOQSFl',45,182,-1125,35),(630,'bOQSFl',46,182,-1125,35),(631,'bOQSFl',35,182,3375,35),(632,'bOQSFl',35,184,-4000,46),(633,'bOQSFl',46,184,4000,46),(634,'bOQSFl',44,185,-183.33,46),(635,'bOQSFl',45,185,-183.33,46),(636,'bOQSFl',46,185,366.67,46),(637,'bOQSFl',35,186,-3250,45),(638,'bOQSFl',44,186,-3250,45),(639,'bOQSFl',46,186,-3250,45),(640,'bOQSFl',45,186,9750,45),(641,'bOQSFl',46,187,-180,45),(642,'bOQSFl',45,187,180,45),(643,'bOQSFl',35,189,-407.5,44),(644,'bOQSFl',45,189,-407.5,44),(645,'bOQSFl',46,189,-407.5,44),(646,'bOQSFl',44,189,1222.5,44),(647,'bOQSFl',35,190,-37.5,45),(648,'bOQSFl',44,190,-37.5,45),(649,'bOQSFl',46,190,-37.5,45),(650,'bOQSFl',45,190,112.5,45),(651,'bOQSFl',35,191,-355,44),(652,'bOQSFl',45,191,-355,44),(653,'bOQSFl',46,191,-355,44),(654,'bOQSFl',44,191,1065,44),(655,'bOQSFl',35,192,-2188.75,44),(656,'bOQSFl',45,192,-2188.75,44),(657,'bOQSFl',46,192,-2188.75,44),(658,'bOQSFl',44,192,6566.25,44),(659,'bOQSFl',44,193,-231.5,35),(660,'bOQSFl',45,193,-231.5,35),(661,'bOQSFl',46,193,-231.5,35),(662,'bOQSFl',35,193,694.5,35),(663,'bOQSFl',35,194,-750,44),(664,'bOQSFl',44,194,750,44),(665,'bOQSFl',35,195,-283.75,44),(666,'bOQSFl',45,195,-283.75,44),(667,'bOQSFl',46,195,-283.75,44),(668,'bOQSFl',44,195,851.25,44),(669,'bOQSFl',35,196,-1819.5,44),(670,'bOQSFl',45,196,-1819.5,44),(671,'bOQSFl',46,196,-1819.5,44),(672,'bOQSFl',44,196,5458.5,44),(673,'bOQSFl',35,197,-205,44),(674,'bOQSFl',44,197,205,44),(681,'93XXiM',35,178,-375,37),(682,'93XXiM',37,178,375,37);
/*!40000 ALTER TABLE `Balance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `expenseId` int NOT NULL AUTO_INCREMENT,
  `expenseDate` datetime NOT NULL,
  `expenseDesc` varchar(350) NOT NULL,
  `expenseAmount` float NOT NULL,
  `expensePaidBy` int NOT NULL,
  `expenseSplitBw` varchar(2000) NOT NULL,
  `tripId` varchar(6) NOT NULL,
  `expenseSelf` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`expenseId`),
  KEY `expensePaidBy` (`expensePaidBy`),
  KEY `tripId` (`tripId`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`expensePaidBy`) REFERENCES `users` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`tripId`) REFERENCES `trips` (`tripIdShared`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (3,'2025-01-11 00:00:00','Zostel-Mumbai',7837,37,'[{\"userId\": 35, \"amount\": 3918.5}, {\"userId\": 37, \"amount\": 3918.5}]','ueQdUr',0),(4,'2025-01-02 00:00:00','Flights-Bangalore-Mumbai',9988,37,'[{\"userId\": 35, \"amount\": 4994.0}, {\"userId\": 37, \"amount\": 4994.0}]','ueQdUr',0),(7,'2025-01-16 00:00:00','Return flights bom-blr ',12294,37,'[{\"userId\": 35, \"amount\": 6147.0}, {\"userId\": 37, \"amount\": 6147.0}]','ueQdUr',0),(8,'2025-01-18 00:00:00','Train Ahm to Bombay',2246,35,'[{\"userId\": 35, \"amount\": 1123.0}, {\"userId\": 37, \"amount\": 1123.0}]','ueQdUr',0),(12,'2025-01-21 00:00:00','Cab to airport bng',1065,37,'[{\"userId\": 35, \"amount\": 532.5}, {\"userId\": 37, \"amount\": 532.5}]','ueQdUr',0),(13,'2025-01-22 00:00:00','Coffee-Zostel',100,37,'[{\"userId\": 35, \"amount\": 50.0}, {\"userId\": 37, \"amount\": 50.0}]','ueQdUr',0),(14,'2025-01-22 00:00:00','Cigz',100,35,'[{\"userId\": 35, \"amount\": 100.0}]','ueQdUr',1),(15,'2025-01-22 00:00:00','auto to zostel',114,35,'[{\"userId\": 35, \"amount\": 57.0}, {\"userId\": 37, \"amount\": 57.0}]','ueQdUr',0),(16,'2025-01-22 00:00:00','Food ',200,37,'[{\"userId\": 35, \"amount\": 100.0}, {\"userId\": 37, \"amount\": 100.0}]','ueQdUr',0),(19,'2025-01-22 00:00:00','Beer',720,35,'[{\"userId\": 35, \"amount\": 360.0}, {\"userId\": 37, \"amount\": 360.0}]','ueQdUr',0),(20,'2025-01-22 00:00:00','Petrol+Misc marine drive',250,35,'[{\"userId\": 35, \"amount\": 125.0}, {\"userId\": 37, \"amount\": 125.0}]','ueQdUr',0),(21,'2025-01-22 00:00:00','Krishna Medicals (Snacks)',160,35,'[{\"userId\": 35, \"amount\": 80.0}, {\"userId\": 37, \"amount\": 80.0}]','ueQdUr',0),(22,'2025-01-23 00:00:00','IRCTC cancellation',120,35,'[{\"userId\": 35, \"amount\": 60.0}, {\"userId\": 37, \"amount\": 60.0}]','ueQdUr',0),(23,'2025-01-23 00:00:00','ELCO',300,35,'[{\"userId\": 35, \"amount\": 150.0}, {\"userId\": 37, \"amount\": 150.0}]','ueQdUr',0),(24,'2025-01-23 00:00:00','Tops-Fake Zara shit',500,35,'[{\"userId\": 37, \"amount\": 500.0}]','ueQdUr',0),(25,'2025-01-23 00:00:00','Chicken Tandoori',240,35,'[{\"userId\": 35, \"amount\": 120.0}, {\"userId\": 37, \"amount\": 120.0}]','ueQdUr',0),(26,'2025-01-23 00:00:00','Cab to Bastian-1',304,35,'[{\"userId\": 35, \"amount\": 152.0}, {\"userId\": 37, \"amount\": 152.0}]','ueQdUr',0),(27,'2025-01-23 00:00:00','Bastian 1 - Bastian 2',126,35,'[{\"userId\": 35, \"amount\": 63.0}, {\"userId\": 37, \"amount\": 63.0}]','ueQdUr',0),(28,'2025-01-23 00:00:00','145',2329,35,'[{\"userId\": 35, \"amount\": 1164.5}, {\"userId\": 37, \"amount\": 1164.5}]','ueQdUr',0),(29,'2025-01-24 00:00:00','Coffee+Misc',150,35,'[{\"userId\": 35, \"amount\": 75.0}, {\"userId\": 37, \"amount\": 75.0}]','ueQdUr',0),(30,'2025-01-24 00:00:00','Cab to temple',189,35,'[{\"userId\": 35, \"amount\": 94.5}, {\"userId\": 37, \"amount\": 94.5}]','ueQdUr',0),(31,'2025-01-24 00:00:00','Another Cab (Rakesh Chauthilal)?',383,35,'[{\"userId\": 35, \"amount\": 191.5}, {\"userId\": 37, \"amount\": 191.5}]','ueQdUr',0),(32,'2025-01-24 00:00:00','Alc',1080,35,'[{\"userId\": 35, \"amount\": 540.0}, {\"userId\": 37, \"amount\": 540.0}]','ueQdUr',0),(33,'2025-01-24 00:00:00','Permit+misc',135,35,'[{\"userId\": 35, \"amount\": 67.5}, {\"userId\": 37, \"amount\": 67.5}]','ueQdUr',0),(34,'2025-01-24 00:00:00','Snacks for bus',150,35,'[{\"userId\": 35, \"amount\": 75.0}, {\"userId\": 37, \"amount\": 75.0}]','ueQdUr',0),(35,'2025-01-24 00:00:00','Bus Dinner',295,35,'[{\"userId\": 35, \"amount\": 147.5}, {\"userId\": 37, \"amount\": 147.5}]','ueQdUr',0),(36,'2025-01-24 00:00:00','Train snacks + Cab to airport',220,35,'[{\"userId\": 35, \"amount\": 110.0}, {\"userId\": 37, \"amount\": 110.0}]','ueQdUr',0),(37,'2025-01-26 00:00:00','Bus back home',600,35,'[{\"userId\": 35, \"amount\": 300.0}, {\"userId\": 37, \"amount\": 300.0}]','ueQdUr',0),(40,'2024-11-27 00:00:00','Coldplay-1-VR',6950,35,'[{\"userId\": 35, \"amount\": 6950.0}]','ueQdUr',1),(41,'2024-11-27 00:00:00','Coldplay-1-AV',7350,37,'[{\"userId\": 37, \"amount\": 7350.0}]','ueQdUr',1),(43,'2025-01-22 00:00:00',' Bike rental (400 helmet + late charge)',1450,35,'[{\"userId\": 35, \"amount\": 725.0}, {\"userId\": 37, \"amount\": 725.0}]','ueQdUr',0),(44,'2025-01-27 00:00:00','Auto from bus stand to hsr ',50,37,'[{\"userId\": 35, \"amount\": 25.0}, {\"userId\": 37, \"amount\": 25.0}]','ueQdUr',0),(46,'2025-01-27 00:00:00','Zomato ahm ',460,37,'[{\"userId\": 35, \"amount\": 230.0}, {\"userId\": 37, \"amount\": 230.0}]','ueQdUr',0),(47,'2025-01-27 00:00:00','Blinkit ahm',460,37,'[{\"userId\": 35, \"amount\": 230.0}, {\"userId\": 37, \"amount\": 230.0}]','ueQdUr',0),(48,'2025-01-27 00:00:00','Zostel tea',86,37,'[{\"userId\": 35, \"amount\": 43.0}, {\"userId\": 37, \"amount\": 43.0}]','ueQdUr',0),(49,'2025-01-27 00:00:00','Kirti vada pav ',90,37,'[{\"userId\": 35, \"amount\": 45.0}, {\"userId\": 37, \"amount\": 45.0}]','ueQdUr',0),(50,'2025-01-27 00:00:00','Bus to ahm ',5072,37,'[{\"userId\": 35, \"amount\": 2536.0}, {\"userId\": 37, \"amount\": 2536.0}]','ueQdUr',0),(51,'2025-01-27 00:00:00','Ganapati temple special entrance + prasad',300,37,'[{\"userId\": 35, \"amount\": 150.0}, {\"userId\": 37, \"amount\": 150.0}]','ueQdUr',0),(52,'2025-01-27 00:00:00','Zostel zomato breakfast ',500,37,'[{\"userId\": 35, \"amount\": 250.0}, {\"userId\": 37, \"amount\": 250.0}]','ueQdUr',0),(53,'2025-01-27 00:00:00','Hill road petrol ',150,37,'[{\"userId\": 35, \"amount\": 75.0}, {\"userId\": 37, \"amount\": 75.0}]','ueQdUr',0),(54,'2025-01-27 00:00:00','Clips for vaishu ',120,37,'[{\"userId\": 35, \"amount\": 120.0}]','ueQdUr',0),(55,'2025-01-27 00:00:00','Photos',230,37,'[{\"userId\": 35, \"amount\": 115.0}, {\"userId\": 37, \"amount\": 115.0}]','ueQdUr',0),(58,'2025-01-28 00:00:00','Misc cash spent ',180,37,'[{\"userId\": 35, \"amount\": 90.0}, {\"userId\": 37, \"amount\": 90.0}]','ueQdUr',0),(61,'2025-02-01 00:00:00','Pakoda in katra',170,35,'[{\"userId\": 35, \"amount\": 170.0}]','nv120j',1),(62,'2025-02-02 00:00:00','Helicopter ',4420,35,'[{\"userId\": 35, \"amount\": 4420.0}]','nv120j',1),(63,'2025-02-02 00:00:00','Prasad ',1700,35,'[{\"userId\": 35, \"amount\": 1700.0}]','nv120j',1),(64,'2025-02-02 00:00:00','Scammer pithu',440,35,'[{\"userId\": 35, \"amount\": 440.0}]','nv120j',1),(65,'2025-02-02 00:00:00','Bhaironath prasad',200,35,'[{\"userId\": 35, \"amount\": 200.0}]','nv120j',1),(66,'2025-02-02 00:00:00','Samosa, tea bhairo',160,35,'[{\"userId\": 35, \"amount\": 160.0}]','nv120j',1),(67,'2025-02-02 00:00:00','Dry fruits',1780,35,'[{\"userId\": 35, \"amount\": 1780.0}]','nv120j',1),(68,'2025-02-02 00:00:00','Auto door hanger+prasad for gift+chalisa+auto return',790,35,'[{\"userId\": 35, \"amount\": 790.0}]','nv120j',1),(69,'2025-02-02 00:00:00','Nathu’s food',770,35,'[{\"userId\": 35, \"amount\": 770.0}]','nv120j',1),(70,'2025-01-31 00:00:00','VR flights',18310,35,'[{\"userId\": 35, \"amount\": 18310.0}]','nv120j',1),(71,'2025-02-03 00:00:00','Food on way manali',1040,35,'[{\"userId\": 35, \"amount\": 1040.0}]','nv120j',1),(72,'2025-02-03 00:00:00','Water can',180,35,'[{\"userId\": 35, \"amount\": 180.0}]','nv120j',1),(73,'2025-02-04 00:00:00','Horse to top',1200,35,'[{\"userId\": 35, \"amount\": 1200.0}]','nv120j',1),(74,'2025-02-04 00:00:00','Chai maggi',200,35,'[{\"userId\": 35, \"amount\": 200.0}]','nv120j',1),(75,'2025-02-04 00:00:00','Corn',120,35,'[{\"userId\": 35, \"amount\": 120.0}]','nv120j',1),(76,'2025-02-04 00:00:00','Lunch manali',1400,35,'[{\"userId\": 35, \"amount\": 1400.0}]','nv120j',1),(77,'2025-02-04 00:00:00','Mall road shopping',750,35,'[{\"userId\": 35, \"amount\": 750.0}]','nv120j',1),(78,'2025-02-06 00:00:00','Holiday home food',4000,35,'[{\"userId\": 35, \"amount\": 4000.0}]','nv120j',1),(80,'2025-03-16 00:00:00','Stay jyoti ',5800,37,'[{\"userId\": 35, \"amount\": 2900.0}, {\"userId\": 37, \"amount\": 2900.0}]','bx7dc0',0),(81,'2025-03-16 00:00:00','Cigs @ airport ',380,37,'[{\"userId\": 35, \"amount\": 190.0}, {\"userId\": 37, \"amount\": 190.0}]','bx7dc0',0),(82,'2025-03-16 00:00:00','Zomato ',1463,37,'[{\"userId\": 35, \"amount\": 731.5}, {\"userId\": 37, \"amount\": 731.5}]','bx7dc0',0),(83,'2025-03-16 00:00:00','Autos',286,37,'[{\"userId\": 35, \"amount\": 143.0}, {\"userId\": 37, \"amount\": 143.0}]','bx7dc0',0),(84,'2025-03-16 00:00:00','Cab to airport ',1024,37,'[{\"userId\": 35, \"amount\": 512.0}, {\"userId\": 37, \"amount\": 512.0}]','bx7dc0',0),(85,'2025-03-16 00:00:00','Cab from airport ',855,37,'[{\"userId\": 35, \"amount\": 427.5}, {\"userId\": 37, \"amount\": 427.5}]','bx7dc0',0),(86,'2025-03-16 00:00:00','Cash spent ',500,37,'[{\"userId\": 35, \"amount\": 250.0}, {\"userId\": 37, \"amount\": 250.0}]','bx7dc0',0),(87,'2025-03-24 00:00:00','Elco',180,35,'[{\"userId\": 35, \"amount\": 90.0}, {\"userId\": 37, \"amount\": 90.0}]','bx7dc0',0),(88,'2025-03-24 00:00:00','Cabs',888,35,'[{\"userId\": 35, \"amount\": 444.0}, {\"userId\": 37, \"amount\": 444.0}]','bx7dc0',0),(89,'2025-03-24 00:00:00','Cabs',131,35,'[{\"userId\": 35, \"amount\": 65.5}, {\"userId\": 37, \"amount\": 65.5}]','bx7dc0',0),(90,'2025-03-24 00:00:00','Room brevistay ',725,35,'[{\"userId\": 35, \"amount\": 362.5}, {\"userId\": 37, \"amount\": 362.5}]','bx7dc0',0),(91,'2025-03-24 00:00:00','Airport food ',600,35,'[{\"userId\": 35, \"amount\": 300.0}, {\"userId\": 37, \"amount\": 300.0}]','bx7dc0',0),(92,'2025-03-24 00:00:00','Toit',1446,35,'[{\"userId\": 35, \"amount\": 723.0}, {\"userId\": 37, \"amount\": 723.0}]','bx7dc0',0),(93,'2025-03-24 00:00:00','Blue tokai ',560,35,'[{\"userId\": 35, \"amount\": 280.0}, {\"userId\": 37, \"amount\": 280.0}]','bx7dc0',0),(94,'2025-03-16 00:00:00','Cash spent ',450,37,'[{\"userId\": 35, \"amount\": 225.0}, {\"userId\": 37, \"amount\": 225.0}]','bx7dc0',1),(95,'2025-03-24 00:00:00','Hill road ',450,35,'[{\"userId\": 35, \"amount\": 225.0}, {\"userId\": 37, \"amount\": 225.0}]','bx7dc0',0),(96,'2025-05-01 00:00:00','Infinity Krabi stay',6724,37,'[{\"userId\": 35, \"amount\": 3362.0}, {\"userId\": 37, \"amount\": 3362.0}]','93XXiM',0),(97,'2025-05-01 00:00:00','Flight to Krabi',26630,35,'[{\"userId\": 35, \"amount\": 13315.0}, {\"userId\": 37, \"amount\": 13315.0}]','93XXiM',0),(98,'2025-05-01 00:00:00','Cafatel by SANKARA',2511,35,'[{\"userId\": 35, \"amount\": 1255.5}, {\"userId\": 37, \"amount\": 1255.5}]','93XXiM',0),(107,'2025-05-08 00:00:00','Raincoats x2',460,37,'[{\"userId\": 35, \"amount\": 230.0}, {\"userId\": 37, \"amount\": 230.0}]','93XXiM',0),(108,'2025-05-08 00:00:00','Cab to airport ',1092,37,'[{\"userId\": 35, \"amount\": 546.0}, {\"userId\": 37, \"amount\": 546.0}]','93XXiM',0),(109,'2025-05-08 00:00:00','Food on plane ',400,37,'[{\"userId\": 35, \"amount\": 200.0}, {\"userId\": 37, \"amount\": 200.0}]','93XXiM',0),(110,'2025-05-08 00:00:00','Shuttle from airport to Sakara',777.7,35,'[{\"userId\": 35, \"amount\": 388.85}, {\"userId\": 37, \"amount\": 388.85}]','93XXiM',0),(111,'2025-05-09 00:00:00','711',140,35,'[{\"userId\": 35, \"amount\": 70.0}, {\"userId\": 37, \"amount\": 70.0}]','93XXiM',0),(112,'2025-05-09 00:00:00','Juice ',259.2,35,'[{\"userId\": 35, \"amount\": 129.6}, {\"userId\": 37, \"amount\": 129.6}]','93XXiM',0),(113,'2025-05-09 00:00:00','Bike ',1296.2,35,'[{\"userId\": 35, \"amount\": 648.1}, {\"userId\": 37, \"amount\": 648.1}]','93XXiM',0),(114,'2025-05-09 00:00:00','Can to infinity ',212.6,35,'[{\"userId\": 35, \"amount\": 106.3}, {\"userId\": 37, \"amount\": 106.3}]','93XXiM',0),(115,'2025-05-09 00:00:00','Beer + roach ',430.3,35,'[{\"userId\": 35, \"amount\": 215.15}, {\"userId\": 37, \"amount\": 215.15}]','93XXiM',0),(116,'2025-05-09 00:00:00','White lily ',648.1,35,'[{\"userId\": 35, \"amount\": 324.05}, {\"userId\": 37, \"amount\": 324.05}]','93XXiM',0),(117,'2025-05-09 00:00:00','Joint ventures 5g ',1062.9,35,'[{\"userId\": 35, \"amount\": 531.45}, {\"userId\": 37, \"amount\": 531.45}]','93XXiM',0),(118,'2025-05-09 00:00:00','Potato smash night market ',256.6,35,'[{\"userId\": 35, \"amount\": 128.3}, {\"userId\": 37, \"amount\": 128.3}]','93XXiM',0),(119,'2025-05-09 00:00:00','Cocktails',518.5,35,'[{\"userId\": 35, \"amount\": 259.25}, {\"userId\": 37, \"amount\": 259.25}]','93XXiM',0),(120,'2025-05-10 00:00:00','Railay beach ',1036.9,35,'[{\"userId\": 35, \"amount\": 518.45}, {\"userId\": 37, \"amount\": 518.45}]','93XXiM',0),(121,'2025-05-10 00:00:00','Railay beach drinks ',440.7,35,'[{\"userId\": 35, \"amount\": 220.35}, {\"userId\": 37, \"amount\": 220.35}]','93XXiM',0),(122,'2025-05-10 00:00:00','Railay beach food',933.2,35,'[{\"userId\": 35, \"amount\": 466.6}, {\"userId\": 37, \"amount\": 466.6}]','93XXiM',0),(123,'2025-05-10 00:00:00','Railay beach ice cream + water ',362.9,35,'[{\"userId\": 35, \"amount\": 181.45}, {\"userId\": 37, \"amount\": 181.45}]','93XXiM',0),(124,'2025-05-10 00:00:00','Railay beach coke',85.5,35,'[{\"userId\": 35, \"amount\": 42.75}, {\"userId\": 37, \"amount\": 42.75}]','93XXiM',0),(125,'2025-05-10 00:00:00','Railay beach auto back to hotel ',259.2,35,'[{\"userId\": 35, \"amount\": 129.6}, {\"userId\": 37, \"amount\": 129.6}]','93XXiM',0),(126,'2025-05-10 00:00:00','Flight to Mumbai ',33485,37,'[{\"userId\": 35, \"amount\": 16742.5}, {\"userId\": 37, \"amount\": 16742.5}]','93XXiM',0),(127,'2025-05-11 00:00:00','Dang doe ding viewpoint ',362.2,35,'[{\"userId\": 35, \"amount\": 181.1}, {\"userId\": 37, \"amount\": 181.1}]','93XXiM',0),(128,'2025-05-11 00:00:00','7 11',103.5,35,'[{\"userId\": 35, \"amount\": 51.75}, {\"userId\": 37, \"amount\": 51.75}]','93XXiM',0),(129,'2025-05-11 00:00:00','Petrol',155.2,35,'[{\"userId\": 35, \"amount\": 77.6}, {\"userId\": 37, \"amount\": 77.6}]','93XXiM',0),(130,'2025-05-11 00:00:00','Can to aonang ',204.4,35,'[{\"userId\": 35, \"amount\": 102.2}, {\"userId\": 37, \"amount\": 102.2}]','93XXiM',0),(131,'2025-05-11 00:00:00','Beer',310.5,35,'[{\"userId\": 35, \"amount\": 155.25}, {\"userId\": 37, \"amount\": 155.25}]','93XXiM',0),(132,'2025-05-11 00:00:00','Aonang eco inn ',1825,37,'[{\"userId\": 35, \"amount\": 912.5}, {\"userId\": 37, \"amount\": 912.5}]','93XXiM',0),(133,'2025-05-11 00:00:00','Aonang eco inn scooter',646.8,37,'[{\"userId\": 35, \"amount\": 323.4}, {\"userId\": 37, \"amount\": 323.4}]','93XXiM',0),(134,'2025-05-12 00:00:00','Transfer to Koh lanta ',2554.8,35,'[{\"userId\": 35, \"amount\": 1277.4}, {\"userId\": 37, \"amount\": 1277.4}]','93XXiM',0),(135,'2025-05-12 00:00:00','Food @ koh lanta transfer (lunch)',357.7,35,'[{\"userId\": 35, \"amount\": 178.85}, {\"userId\": 37, \"amount\": 178.85}]','93XXiM',0),(136,'2025-05-12 00:00:00','Bike koh lanta ',1277.4,35,'[{\"userId\": 35, \"amount\": 638.7}, {\"userId\": 37, \"amount\": 638.7}]','93XXiM',0),(137,'2025-05-12 00:00:00','Dinner @ lanta walking street ',1277.4,35,'[{\"userId\": 35, \"amount\": 638.7}, {\"userId\": 37, \"amount\": 638.7}]','93XXiM',0),(138,'2025-05-13 00:00:00','711',643.8,35,'[{\"userId\": 35, \"amount\": 321.9}, {\"userId\": 37, \"amount\": 321.9}]','93XXiM',0),(139,'2025-05-13 00:00:00','Cops ',1277.4,35,'[{\"userId\": 35, \"amount\": 638.7}, {\"userId\": 37, \"amount\": 638.7}]','93XXiM',0),(140,'2025-05-13 00:00:00','Lighter',25.5,35,'[{\"userId\": 35, \"amount\": 12.75}, {\"userId\": 37, \"amount\": 12.75}]','93XXiM',1),(141,'2025-05-13 00:00:00','Fuel',306.6,35,'[{\"userId\": 35, \"amount\": 153.3}, {\"userId\": 37, \"amount\": 153.3}]','93XXiM',0),(142,'2025-05-13 00:00:00','Dinner Koh lanta',638.7,35,'[{\"userId\": 35, \"amount\": 319.35}, {\"userId\": 37, \"amount\": 319.35}]','93XXiM',0),(143,'2025-05-13 00:00:00','SIM card ',1019.3,35,'[{\"userId\": 35, \"amount\": 509.65}, {\"userId\": 37, \"amount\": 509.65}]','93XXiM',0),(144,'2025-05-14 00:00:00','711',30.7,35,'[{\"userId\": 35, \"amount\": 15.35}, {\"userId\": 37, \"amount\": 15.35}]','93XXiM',0),(146,'2025-05-14 00:00:00','Petrol to fill Koh lanta bike ',191.6,35,'[{\"userId\": 35, \"amount\": 95.8}, {\"userId\": 37, \"amount\": 95.8}]','93XXiM',0),(147,'2025-05-15 00:00:00','Cops 2',1293.7,35,'[{\"userId\": 35, \"amount\": 646.85}, {\"userId\": 37, \"amount\": 646.85}]','93XXiM',0),(148,'2025-05-16 00:00:00','711',181.4,35,'[{\"userId\": 35, \"amount\": 90.7}, {\"userId\": 37, \"amount\": 90.7}]','93XXiM',0),(149,'2025-05-16 00:00:00','Petrol phuket',383.2,35,'[{\"userId\": 35, \"amount\": 191.6}, {\"userId\": 37, \"amount\": 191.6}]','93XXiM',0),(150,'2025-05-16 00:00:00','Grab to 3 monkeys ',825.2,35,'[{\"userId\": 35, \"amount\": 412.6}, {\"userId\": 37, \"amount\": 412.6}]','93XXiM',0),(151,'2025-05-16 00:00:00','hbd dinner @3 monkeys ',2493.4,35,'[{\"userId\": 35, \"amount\": 1246.7}, {\"userId\": 37, \"amount\": 1246.7}]','93XXiM',1),(152,'2025-05-16 00:00:00','Weed phuket',383.2,35,'[{\"userId\": 35, \"amount\": 191.6}, {\"userId\": 37, \"amount\": 191.6}]','93XXiM',0),(153,'2025-05-16 00:00:00','7k aish withdrawal charges ',562,37,'[{\"userId\": 35, \"amount\": 281.0}, {\"userId\": 37, \"amount\": 281.0}]','93XXiM',0),(154,'2025-05-17 00:00:00','Cab to airport Phuket ',1121.5,35,'[{\"userId\": 35, \"amount\": 560.75}, {\"userId\": 37, \"amount\": 560.75}]','93XXiM',0),(155,'2025-05-17 00:00:00','Food @phuket airport sandwich ',434.3,35,'[{\"userId\": 35, \"amount\": 217.15}, {\"userId\": 37, \"amount\": 217.15}]','93XXiM',0),(156,'2025-05-17 00:00:00','Duty free',2832,37,'[{\"userId\": 35, \"amount\": 1416.0}, {\"userId\": 37, \"amount\": 1416.0}]','93XXiM',0),(157,'2025-05-17 00:00:00','Safe wrap ',400,37,'[{\"userId\": 35, \"amount\": 200.0}, {\"userId\": 37, \"amount\": 200.0}]','93XXiM',0),(158,'2025-05-08 00:00:00','Travel insurance icici ',1106,37,'[{\"userId\": 35, \"amount\": 553.0}, {\"userId\": 37, \"amount\": 553.0}]','93XXiM',0),(160,'2025-05-12 00:00:00','Koh lanta lanta pura resort ',6433,37,'[{\"userId\": 35, \"amount\": 3216.5}, {\"userId\": 37, \"amount\": 3216.5}]','93XXiM',0),(161,'2025-05-14 00:00:00','Seabed grand Phuket ',10532,37,'[{\"userId\": 35, \"amount\": 5266.0}, {\"userId\": 37, \"amount\": 5266.0}]','93XXiM',0),(163,'2025-05-16 00:00:00','Phuket bags ',10883.3,35,'[{\"userId\": 35, \"amount\": 5441.65}, {\"userId\": 37, \"amount\": 5441.65}]','93XXiM',0),(164,'2025-05-16 00:00:00','Phuket Nike stuff',3576.7,35,'[{\"userId\": 35, \"amount\": 1788.35}, {\"userId\": 37, \"amount\": 1788.35}]','93XXiM',1),(165,'2025-05-15 00:00:00','711',117.5,35,'[{\"userId\": 35, \"amount\": 58.75}, {\"userId\": 37, \"amount\": 58.75}]','93XXiM',0),(166,'2025-05-15 00:00:00','Rice ',102.2,35,'[{\"userId\": 35, \"amount\": 51.1}, {\"userId\": 37, \"amount\": 51.1}]','93XXiM',0),(167,'2025-05-15 00:00:00','Promethe cafe frappe ',255.5,35,'[{\"userId\": 35, \"amount\": 127.75}, {\"userId\": 37, \"amount\": 127.75}]','93XXiM',0),(168,'2025-05-15 00:00:00','MCD',355.1,35,'[{\"userId\": 35, \"amount\": 177.55}, {\"userId\": 37, \"amount\": 177.55}]','93XXiM',0),(169,'2025-05-14 00:00:00','Ferry',4087.6,35,'[{\"userId\": 35, \"amount\": 2043.8}, {\"userId\": 37, \"amount\": 2043.8}]','93XXiM',0),(170,'2025-05-08 00:00:00','Money withdrawal from bank tax ',1100,35,'[{\"userId\": 35, \"amount\": 550.0}, {\"userId\": 37, \"amount\": 550.0}]','93XXiM',0),(171,'2025-05-08 00:00:00','MTR ',1500,37,'[{\"userId\": 35, \"amount\": 750.0}, {\"userId\": 37, \"amount\": 750.0}]','93XXiM',0),(172,'2025-05-19 00:00:00','Mumbai cab ',336,35,'[{\"userId\": 35, \"amount\": 168.0}, {\"userId\": 37, \"amount\": 168.0}]','93XXiM',0),(173,'2025-05-19 00:00:00','Mumbai cab ',375,35,'[{\"userId\": 35, \"amount\": 187.5}, {\"userId\": 37, \"amount\": 187.5}]','93XXiM',0),(174,'2025-05-19 00:00:00','Mumbai cab ',451,35,'[{\"userId\": 35, \"amount\": 225.5}, {\"userId\": 37, \"amount\": 225.5}]','93XXiM',0),(175,'2025-05-19 00:00:00','Mumbai food lunch',700,37,'[{\"userId\": 35, \"amount\": 350.0}, {\"userId\": 37, \"amount\": 350.0}]','93XXiM',0),(176,'2025-05-11 00:00:00','Weed + chocolate joint ventures ',1960.5,35,'[{\"userId\": 35, \"amount\": 980.25}, {\"userId\": 37, \"amount\": 980.25}]','93XXiM',0),(177,'2025-05-12 00:00:00','711 cheetos misc ',656.1,35,'[{\"userId\": 35, \"amount\": 328.05}, {\"userId\": 37, \"amount\": 328.05}]','93XXiM',0),(178,'2025-06-03 00:00:00','Cab back from jimmis',750,37,'[{\"userId\": 35, \"amount\": 375.0}, {\"userId\": 37, \"amount\": 375.0}]','93XXiM',0),(181,'2025-07-07 00:00:00','Tickets buying ',11387,37,'[{\"userId\": 37, \"amount\": 11387.0}]','7fa5rf',0),(182,'2025-09-19 00:00:00','Petrol',4500,35,'[{\"userId\": 35, \"amount\": 1125.0}, {\"userId\": 44, \"amount\": 1125.0}, {\"userId\": 45, \"amount\": 1125.0}, {\"userId\": 46, \"amount\": 1125.0}]','bOQSFl',0),(184,'2025-09-18 00:00:00','Dro',8000,46,'[{\"userId\": 35, \"amount\": 4000.0}, {\"userId\": 46, \"amount\": 4000.0}]','bOQSFl',0),(185,'2025-09-19 00:00:00','Tata coffee',550,46,'[{\"userId\": 44, \"amount\": 183.33}, {\"userId\": 45, \"amount\": 183.33}, {\"userId\": 46, \"amount\": 183.33}]','bOQSFl',0),(186,'2025-09-20 00:00:00','Airbnb',13000,45,'[{\"userId\": 35, \"amount\": 3250.0}, {\"userId\": 44, \"amount\": 3250.0}, {\"userId\": 45, \"amount\": 3250.0}, {\"userId\": 46, \"amount\": 3250.0}]','bOQSFl',0),(187,'2025-09-20 00:00:00','Breakfast-1',360,45,'[{\"userId\": 45, \"amount\": 180.0}, {\"userId\": 46, \"amount\": 180.0}]','bOQSFl',0),(189,'2025-09-19 00:00:00','Biryani mysore',1630,44,'[{\"userId\": 35, \"amount\": 407.5}, {\"userId\": 44, \"amount\": 407.5}, {\"userId\": 45, \"amount\": 407.5}, {\"userId\": 46, \"amount\": 407.5}]','bOQSFl',0),(190,'2025-09-19 00:00:00','Snacks and shit',150,45,'[{\"userId\": 35, \"amount\": 37.5}, {\"userId\": 44, \"amount\": 37.5}, {\"userId\": 45, \"amount\": 37.5}, {\"userId\": 46, \"amount\": 37.5}]','bOQSFl',0),(191,'2025-09-19 00:00:00','Dinner virajpet',1420,44,'[{\"userId\": 35, \"amount\": 355.0}, {\"userId\": 44, \"amount\": 355.0}, {\"userId\": 45, \"amount\": 355.0}, {\"userId\": 46, \"amount\": 355.0}]','bOQSFl',0),(192,'2025-09-19 00:00:00','Alc',8755,44,'[{\"userId\": 35, \"amount\": 2188.75}, {\"userId\": 44, \"amount\": 2188.75}, {\"userId\": 45, \"amount\": 2188.75}, {\"userId\": 46, \"amount\": 2188.75}]','bOQSFl',0),(193,'2025-09-19 00:00:00','Toll',926,35,'[{\"userId\": 35, \"amount\": 231.5}, {\"userId\": 44, \"amount\": 231.5}, {\"userId\": 45, \"amount\": 231.5}, {\"userId\": 46, \"amount\": 231.5}]','bOQSFl',0),(194,'2025-09-19 00:00:00','FastTag Rechange',750,44,'[{\"userId\": 35, \"amount\": 750.0}]','bOQSFl',0),(195,'2025-09-19 00:00:00','TataCoffee-Coming back',1135,44,'[{\"userId\": 35, \"amount\": 283.75}, {\"userId\": 44, \"amount\": 283.75}, {\"userId\": 45, \"amount\": 283.75}, {\"userId\": 46, \"amount\": 283.75}]','bOQSFl',0),(196,'2025-09-19 00:00:00','Airbnb food+trek',7278,44,'[{\"userId\": 35, \"amount\": 1819.5}, {\"userId\": 44, \"amount\": 1819.5}, {\"userId\": 45, \"amount\": 1819.5}, {\"userId\": 46, \"amount\": 1819.5}]','bOQSFl',0),(197,'2025-09-19 00:00:00','Breakfast day 2-',410,44,'[{\"userId\": 35, \"amount\": 205.0}, {\"userId\": 44, \"amount\": 205.0}]','bOQSFl',0),(198,'2025-09-26 00:00:00','Trek cost',17000,35,'[{\"userId\": 35, \"amount\": 17000.0}]','aQs9dF',0),(202,'2025-09-28 00:00:00','Trek cost',17798,35,'[{\"userId\": 35, \"amount\": 17798.0}]','aQs9dF',1),(203,'2025-09-28 00:00:00','Medical cerificates',250,35,'[{\"userId\": 35, \"amount\": 250.0}]','aQs9dF',1);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `noteId` int NOT NULL AUTO_INCREMENT,
  `note` text NOT NULL,
  `userId` int NOT NULL,
  `tripId` varchar(6) NOT NULL,
  PRIMARY KEY (`noteId`),
  KEY `userId` (`userId`),
  KEY `tripId` (`tripId`),
  CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `notes_ibfk_2` FOREIGN KEY (`tripId`) REFERENCES `trips` (`tripIdShared`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (4,'Contact bike guy to finalise bike. ',35,'93XXiM'),(5,'Order contacts.\nGet money from Papa. \nWash and pack clothes.',35,'93XXiM'),(7,'Cunt slut abused me for not going and filling petrol in the rain even though i told her that the the charge was 50 baht and the minimum petrol pump filling requirement was 60 baht. ',35,'93XXiM'),(9,'1000bt given by aish- 13/05 \n2000bt given by aish- Phuket deposit- 14/05',37,'93XXiM'),(10,'All icici card transactions are left \nFlight to Kolkata \nReturn flights from Phuket to Mumbai ',37,'93XXiM'),(11,'2k bt left-> given to vidish \n8800-> transferred to uncle to add to forex card ',37,'93XXiM');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tripRequest`
--

DROP TABLE IF EXISTS `tripRequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tripRequest` (
  `tripId` varchar(6) NOT NULL,
  `userId` int NOT NULL,
  PRIMARY KEY (`tripId`,`userId`),
  KEY `userIdReq` (`userId`),
  CONSTRAINT `tripIdReq` FOREIGN KEY (`tripId`) REFERENCES `trips` (`tripIdShared`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userIdReq` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tripRequest`
--

LOCK TABLES `tripRequest` WRITE;
/*!40000 ALTER TABLE `tripRequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `tripRequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trips` (
  `tripIdShared` varchar(6) NOT NULL,
  `tripTitle` varchar(150) NOT NULL,
  `currencies` varchar(500) NOT NULL,
  PRIMARY KEY (`tripIdShared`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES ('36p72y','Household','Indian Rupees'),('7fa5rf','Echoes of Earth ','Indian Rupees'),('93XXiM','Thailand May-2025','Thai Baht,Indian Rupees'),('aQs9dF','Rupin Pass','Indian Rupees'),('bOQSFl','Coorg Boys','Indian Rupees'),('bx7dc0','Lollapalloza 2025','Indian Rupees'),('nv120j','Vaishno Devi','Indian Rupees'),('SyMcne','manali','Indian Rupees'),('ueQdUr','Gujrat-Coldplay','Indian Rupees');
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userTrips`
--

DROP TABLE IF EXISTS `userTrips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userTrips` (
  `userId` int NOT NULL,
  `tripId` varchar(6) NOT NULL,
  PRIMARY KEY (`userId`,`tripId`),
  KEY `tripId_idx` (`tripId`),
  CONSTRAINT `tripId` FOREIGN KEY (`tripId`) REFERENCES `trips` (`tripIdShared`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userId` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userTrips`
--

LOCK TABLES `userTrips` WRITE;
/*!40000 ALTER TABLE `userTrips` DISABLE KEYS */;
INSERT INTO `userTrips` VALUES (35,'36p72y'),(37,'7fa5rf'),(35,'93XXiM'),(37,'93XXiM'),(35,'aQs9dF'),(35,'bOQSFl'),(44,'bOQSFl'),(45,'bOQSFl'),(46,'bOQSFl'),(35,'bx7dc0'),(37,'bx7dc0'),(35,'nv120j'),(42,'SyMcne'),(35,'ueQdUr'),(37,'ueQdUr');
/*!40000 ALTER TABLE `userTrips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(100) NOT NULL,
  `email` varchar(250) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `userName_email` (`userName`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (37,'aishvish','millamatew@gmail.com'),(46,'Arooon','test4@test.com'),(45,'Chirra','test3@test.com'),(39,'demoo','demo@demo.com'),(40,'pavankumar','pavankumar24cs@gmail.com\n'),(43,'TestUser1','testuser@test.com'),(41,'vidish97','vidishraj97@gmail.com'),(35,'vidishraj','vidishraj@gmail.com'),(44,'Viggy_Swiggy','test2@test.com'),(42,'vrushti','vrushtip19@gmail.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-28 17:01:21
