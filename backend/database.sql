/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: test_tesis
-- ------------------------------------------------------
-- Server version	10.11.11-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Estudiantes`
--

DROP TABLE IF EXISTS `Estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Estudiantes` (
  `cedula` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `carrera` varchar(255) NOT NULL,
  `correo_electronico` varchar(150) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_registro` date NOT NULL,
  `pago_pendiente` tinyint(1) NOT NULL,
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Estudiantes`
--

LOCK TABLES `Estudiantes` WRITE;
/*!40000 ALTER TABLE `Estudiantes` DISABLE KEYS */;
INSERT INTO `Estudiantes` VALUES
('30.998.394','Jesser','Palma','INFORMATICA','jssr4@gmail.com','0412','2025-05-11','2025-05-11',1);
/*!40000 ALTER TABLE `Estudiantes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pagos`
--

DROP TABLE IF EXISTS `Pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pagos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monto` float NOT NULL,
  `fecha_pago` date NOT NULL,
  `estudiante_cedula` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estudiante_cedula` (`estudiante_cedula`),
  CONSTRAINT `Pagos_ibfk_1` FOREIGN KEY (`estudiante_cedula`) REFERENCES `Estudiantes` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pagos`
--

LOCK TABLES `Pagos` WRITE;
/*!40000 ALTER TABLE `Pagos` DISABLE KEYS */;
INSERT INTO `Pagos` VALUES
(1,100,'2025-05-11','30.998.394');
/*!40000 ALTER TABLE `Pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RegistrosAcceso`
--

DROP TABLE IF EXISTS `RegistrosAcceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `RegistrosAcceso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tarjeta_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `acceso_permitido` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tarjeta_id` (`tarjeta_id`),
  CONSTRAINT `RegistrosAcceso_ibfk_1` FOREIGN KEY (`tarjeta_id`) REFERENCES `TarjetasNFC` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RegistrosAcceso`
--

LOCK TABLES `RegistrosAcceso` WRITE;
/*!40000 ALTER TABLE `RegistrosAcceso` DISABLE KEYS */;
INSERT INTO `RegistrosAcceso` VALUES
(1,1234,'2025-05-10','21:59:07','ENTRADA',1),
(2,1234,'2025-05-10','22:22:00','ENTRADA',1),
(3,1234,'2025-05-10','22:22:03','ENTRADA',1);
/*!40000 ALTER TABLE `RegistrosAcceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TarjetasNFC`
--

DROP TABLE IF EXISTS `TarjetasNFC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `TarjetasNFC` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `estudiante_cedula` varchar(255) DEFAULT NULL,
  `fecha_emision` date NOT NULL,
  `fecha_expiracion` date NOT NULL,
  `activa` tinyint(1) NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `estudiante_cedula` (`estudiante_cedula`),
  CONSTRAINT `TarjetasNFC_ibfk_1` FOREIGN KEY (`estudiante_cedula`) REFERENCES `Estudiantes` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=1235 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TarjetasNFC`
--

LOCK TABLES `TarjetasNFC` WRITE;
/*!40000 ALTER TABLE `TarjetasNFC` DISABLE KEYS */;
INSERT INTO `TarjetasNFC` VALUES
(1234,'30.998.394','2025-05-11','2027-05-11',1);
/*!40000 ALTER TABLE `TarjetasNFC` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UsuariosAdmin`
--

DROP TABLE IF EXISTS `UsuariosAdmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `UsuariosAdmin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `correo_electronico` varchar(150) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UsuariosAdmin`
--

LOCK TABLES `UsuariosAdmin` WRITE;
/*!40000 ALTER TABLE `UsuariosAdmin` DISABLE KEYS */;
INSERT INTO `UsuariosAdmin` VALUES
(1,'Jesser','Palma','jssr3@gmail.com','$2b$12$wpqN94MS0SnsxQ623Uwq.e2RaGYHwYgbilijJy.3g9hJBAYQIe0MO');
/*!40000 ALTER TABLE `UsuariosAdmin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-10 22:23:22
