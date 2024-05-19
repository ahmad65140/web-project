CREATE DATABASE  IF NOT EXISTS `crowdfunding_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `crowdfunding_db`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: crowdfunding_db
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ahmad_admin','ahmad_admin@email.com','scrypt:32768:8:1$lmyyG14bTpbCmIwA$6ef5366caf4ea75dad2a18a47a9bd2fd183ea754ee64393553ed342ff23bc4b91f053be504428bea6e3ab27f2da5ef6299f84e974343f30b2b349c854c9eceab','admin'),(2,'john.smith','johnSmith@email.com','scrypt:32768:8:1$lmyyG14bTpbCmIwA$6ef5366caf4ea75dad2a18a47a9bd2fd183ea754ee64393553ed342ff23bc4b91f053be504428bea6e3ab27f2da5ef6299f84e974343f30b2b349c854c9eceab','admin'),(3,'son_goku','goku@email.com','','user'),(4,'testuser','examplllle@example.com','scrypt:32768:8:1$lmyyG14bTpbCmIwA$6ef5366caf4ea75dad2a18a47a9bd2fd183ea754ee64393553ed342ff23bc4b91f053be504428bea6e3ab27f2da5ef6299f84e974343f30b2b349c854c9eceab','user'),(6,'ghoul','johnith@email.com','scrypt:32768:8:1$L2FEMVd34U2xXQnJ$e732d306e06688bbd684d68da53dcd59050f655ce0c13c07fad7ce11ec9ab2c4bff85ada06042985b96978c40f8ac9fdace151694d7911701b3ce18f7f9cc7ec','user'),(7,'Jiren','Arch.jahamy.mohamed@gmail.com','scrypt:32768:8:1$wbFeHnnxgGGxLJ5y$afbdfce16b0713ec75eb0916d608ecaa6feaf414cd37a2299034fcbd2d8cd29bb957c9d0d74512fdacf7dfb4b18afa1afbbe0f163d6ea736196ea43b6744052a','user'),(8,'Han_lee','han.lee@gmail.com','scrypt:32768:8:1$8BTMaFwcdmPsWz5L$8d013b11efaca27baed466a88ca0d4fa344ea8a5a112bff97a10543ffb2a2157f7cecec55493c80e65d3a7ae672f5b5657023c2ca983367a3508cb4a02c586a5','user');
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

-- Dump completed on 2024-05-19 23:39:49
