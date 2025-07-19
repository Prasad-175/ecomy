-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ecom
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `admindata`
--

DROP TABLE IF EXISTS `admindata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admindata` (
  `adminemail` varchar(255) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `address` text,
  `agree` enum('on','off') DEFAULT NULL,
  `profilepic` varchar(15) DEFAULT NULL,
  `phone_no` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`adminemail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admindata`
--

LOCK TABLES `admindata` WRITE;
/*!40000 ALTER TABLE `admindata` DISABLE KEYS */;
INSERT INTO `admindata` VALUES ('durgaprasaddondapati602@gmail.com','DP','$2b$12$2BkUpxPcuSG8SP5gt8iEEe.xBuMXcwxORTZpQa21DvhV3IKySWJ7W','vuyyuru','on','Rl4Vx3.jpeg','123456789');
/*!40000 ALTER TABLE `admindata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `itemid` binary(16) NOT NULL,
  `itemname` varchar(255) NOT NULL,
  `description` text,
  `quantity` mediumint NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `category` enum('Home appliances','Sports','Electronics','Grocery','Fashion') DEFAULT NULL,
  `imagename` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `added_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`itemid`),
  KEY `added_by` (`added_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (_binary '0à\n]â\ü\Ê!-}\Ó0%','buds','True Wireless Earbuds with 35 Hours Playback, 13mm Drivers, ENx‚Ñ¢ Tech, ASAP‚Ñ¢ Charge, IWP‚Ñ¢ Technology\r\n\r\nRead more at: https://www.boat-lifestyle.com/products/airdopes-alpha-true-wireless-earbuds?variant=41821558734946&country=IN¬§cy=INR&gad_source=1&gad_campaignid=20752090704&gbraid=0AAAAADCnhlyJ3rO6YlvDAzOXChNgH5mCk&gclid=CjwKCAjwyb3DBhBlEiwAqZLe5HpVUKqoMUVuuTFZsnupUBPP96Mb0bXslwiwsIv9_E-sbNfIsBQedBoC6X4QAvD_BwE',4,1000.00,'Electronics','Dt3Yc5.webp','2025-07-10 17:57:05','durgaprasaddondapati602@gmail.com'),(_binary '\√QùÅ`õ\üœçüvoÀ™','iphone','DYNAMIC ISLAND COMES TO IPHONE 15 ‚Äî Dynamic Island bubbles up alerts and Live Activities ‚Äî so you don‚Äôt miss them while you‚Äôre doing something else. You can see who‚Äôs calling, track your next ride, check your flight status, and so much more.\r\nINNOVATIVE DESIGN ‚Äî iPhone 15 features a durable color-infused glass and aluminum design. It‚Äôs splash, water, and dust resistant. The Ceramic Shield front is tougher than any smartphone glass. And the 6.1\" Super Retina XDR display is up to 2x brighter in the sun compared to iPhone 14.\r\n48MP MAIN CAMERA WITH 2X TELEPHOTO ‚Äî The 48MP Main camera shoots in super-high resolution. So it‚Äôs easier than ever to take standout photos with amazing detail. The 2x optical-quality Telephoto lets you frame the perfect close-up.\r\n',6,70000.00,'Electronics','Tg3Is9.webp','2025-07-14 15:47:36','durgaprasaddondapati602@gmail.com');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int unsigned NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) DEFAULT NULL,
  `total_amount` bigint unsigned DEFAULT NULL,
  `quantity` int unsigned DEFAULT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `payment_by` varchar(50) DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`order_id`),
  KEY `order_date` (`order_date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'buds',1000,1,'2025-07-14 16:12:01','durgaprasaddondapati175@gmail.com','vuyyuru'),(2,'buds',1000,1,'2025-07-15 15:33:30','durgaprasaddondapati175@gmail.com','vuyyuru'),(3,'buds',1000,1,'2025-07-15 17:08:30','durgaprasaddondapati175@gmail.com','vuyyuru');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `reviewid` int unsigned NOT NULL AUTO_INCREMENT,
  `review` longtext,
  `rating` enum('1','2','3','4','5') DEFAULT NULL,
  `itemid` binary(16) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reviewid`),
  KEY `itemid` (`itemid`),
  KEY `user` (`user`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`itemid`) REFERENCES `items` (`itemid`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user`) REFERENCES `users` (`useremail`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,'gdfjhagfjag','3',_binary '0à\n]â\ü\Ê!-}\Ó0%','durgaprasaddondapati175@gmail.com','2025-07-16 17:58:21'),(2,'hdgjkqwgke','3',_binary '0à\n]â\ü\Ê!-}\Ó0%','durgaprasaddondapati175@gmail.com','2025-07-16 17:58:31');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `useremail` varchar(50) NOT NULL,
  `address` text NOT NULL,
  `password` varbinary(255) NOT NULL,
  `gender` enum('male','female') DEFAULT NULL,
  PRIMARY KEY (`useremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('dp','durgaprasaddondapati175@gmail.com','vuyyuru',_binary '$2b$12$Y5Uw/e.nIJKhw6NQ8SHwpei02x.ZzgDaqN4pkumR36P32iiWo6DXe','male');
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

-- Dump completed on 2025-07-19 15:30:12
