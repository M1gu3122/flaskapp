-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-10-2024 a las 21:39:29
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `granjahoy`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alertas`
--

CREATE TABLE `alertas` (
  `id_alertas` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alertuser`
--

CREATE TABLE `alertuser` (
  `id_alertas` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_climaticos`
--

CREATE TABLE `datos_climaticos` (
  `id_dato` int(11) NOT NULL,
  `humedad` decimal(5,2) NOT NULL,
  `temperatura` decimal(5,2) NOT NULL,
  `fecha` date NOT NULL,
  `id_galpon` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `datos_climaticos`
--

INSERT INTO `datos_climaticos` (`id_dato`, `humedad`, `temperatura`, `fecha`, `id_galpon`) VALUES
(1, 52.30, 24.33, '2024-08-07', 1),
(2, 60.20, 28.90, '2024-08-08', 2),
(3, 45.00, 22.00, '2024-08-09', 1),
(4, 50.00, 23.00, '2024-08-10', 1),
(5, 55.00, 24.00, '2024-08-11', 2),
(6, 60.00, 25.00, '2024-08-12', 2),
(7, 65.00, 26.00, '2024-08-13', 3),
(8, 64.30, 33.10, '2024-08-17', 6),
(9, 65.50, 24.50, '2024-08-16', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `galpon`
--

CREATE TABLE `galpon` (
  `id_galpon` int(11) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `aves` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `galpon`
--

INSERT INTO `galpon` (`id_galpon`, `capacidad`, `aves`) VALUES
(1, 100, 98),
(2, 120, 110),
(3, 90, 85),
(4, 110, 100),
(5, 130, 125),
(6, 25, 150),
(7, 300, 150),
(8, 400, 200),
(9, 400, 155),
(10, 200, 153),
(11, 100, 50),
(12, 100, 56),
(13, 160, 78),
(14, 230, 175),
(15, 200, 75),
(16, 180, 69),
(17, 200, 150),
(18, 250, 189),
(19, 120, 85),
(20, 150, 75),
(21, 100, 50),
(22, 366, 84),
(23, 0, 0),
(24, 0, 0),
(25, 0, 0),
(26, 0, 0),
(27, 0, 0),
(28, 0, 0),
(29, 40, 23),
(30, 100, 78);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `granja`
--

CREATE TABLE `granja` (
  `id_granja` int(11) NOT NULL,
  `nombre_granja` varchar(100) NOT NULL,
  `contraseña` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `granja`
--

INSERT INTO `granja` (`id_granja`, `nombre_granja`, `contraseña`) VALUES
(1, 'avicampo', 'Admin123'),
(457, 'Migranja', 'Admin123'),
(1254, 'YourFarm', 'Admin123'),
(95198, 'sw', 'Admin123'),
(156165, 'miotragr', 'Admin123'),
(457334, 'Migranja', 'Admin123'),
(561565, 'er', 'Admin123'),
(1139424234, 'YourFarm', 'Admin123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gran_galpon`
--

CREATE TABLE `gran_galpon` (
  `id_granja` int(11) NOT NULL,
  `id_galpon` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `huevos`
--

CREATE TABLE `huevos` (
  `id_recoleccion` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_lote` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `huevos`
--

INSERT INTO `huevos` (`id_recoleccion`, `cantidad`, `fecha`, `id_lote`) VALUES
(1, 30, '2024-07-20', 1),
(2, 40, '2024-07-22', 2),
(3, 35, '2024-07-23', 3),
(4, 50, '2024-07-25', 4),
(5, 45, '2024-07-26', 5),
(6, 60, '2024-07-27', 6),
(7, 55, '2024-07-29', 7),
(8, 70, '2024-07-30', 8),
(9, 65, '2024-08-01', 9),
(10, 80, '2024-08-02', 10),
(11, 75, '2024-08-03', 11),
(12, 90, '2024-08-04', 12),
(13, 85, '2024-08-05', 13),
(14, 100, '2024-08-06', 14),
(15, 95, '2024-08-07', 15),
(16, 110, '2024-08-08', 16),
(17, 105, '2024-08-09', 17),
(18, 120, '2024-08-10', 18),
(19, 115, '2024-08-11', 19),
(20, 125, '2024-08-12', 20),
(21, 22, '2024-08-17', 5),
(23, 300, '2024-08-16', 2),
(24, 150, '2024-09-24', 2),
(25, 177, '2024-09-24', 3),
(26, 150, '2024-09-30', 4),
(27, 150, '2024-09-30', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `id_lote` int(11) NOT NULL,
  `num_aves` int(11) DEFAULT NULL,
  `fecha_ingreso` date NOT NULL,
  `id_galpon` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `lote`
--

INSERT INTO `lote` (`id_lote`, `num_aves`, `fecha_ingreso`, `id_galpon`) VALUES
(1, 11, '2024-07-16', 6),
(2, 18, '2024-08-01', 2),
(3, 20, '2024-08-10', 2),
(4, 25, '2024-08-07', 2),
(5, 35, '2024-08-07', 2),
(6, 42, '2024-08-09', 3),
(7, 42, '2024-08-08', 2),
(8, 24, '2024-08-09', 8),
(9, 54, '2024-08-22', 6),
(10, 13, '2024-08-13', 3),
(11, 30, '2024-08-15', 4),
(12, 25, '2024-08-16', 5),
(13, 40, '2024-08-17', 6),
(14, 50, '2024-08-18', 3),
(15, 27, '2024-08-19', 7),
(16, 33, '2024-08-20', 8),
(17, 44, '2024-08-21', 4),
(18, 21, '2024-08-22', 5),
(19, 37, '2024-08-23', 6),
(20, 29, '2024-08-24', 7),
(21, 22, '2024-08-17', 3),
(22, 24, '2024-09-22', 2),
(23, 14, '2024-09-30', 6),
(24, 25, '2024-09-30', 4),
(25, 54, '2024-09-30', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id_reporte` int(11) NOT NULL,
  `fecha_registro` date NOT NULL,
  `id_lote` int(11) NOT NULL,
  `diagnostico` text DEFAULT NULL,
  `tratamiento_prescrito` text DEFAULT NULL,
  `fecha_inicio_tratamiento` date DEFAULT NULL,
  `fecha_fin_tratamiento` date DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `estado_general` varchar(255) DEFAULT NULL,
  `dosis` varchar(50) DEFAULT NULL,
  `frecuencia_tratamiento` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reportes`
--

INSERT INTO `reportes` (`id_reporte`, `fecha_registro`, `id_lote`, `diagnostico`, `tratamiento_prescrito`, `fecha_inicio_tratamiento`, `fecha_fin_tratamiento`, `id_usuario`, `estado_general`, `dosis`, `frecuencia_tratamiento`) VALUES
(1, '2024-10-11', 1, 'Infeccion respiratoria', 'Antibioticon B', '2024-10-11', '2024-10-18', 3, 'Regular', '10 mg', 'diario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `tipo_usuario` enum('administrador','trabajador','veterinario') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `tipo_usuario`) VALUES
(1, 'administrador'),
(2, 'trabajador'),
(3, 'veterinario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_tareas` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_asignacion` date NOT NULL,
  `estado` enum('Pendiente','En progreso','Completado') NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_tareas`, `descripcion`, `fecha_asignacion`, `estado`, `id_usuario`) VALUES
(1, 'Revisar el suministro de agua', '2024-10-11', 'Pendiente', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombres` varchar(100) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `usuario` varchar(50) NOT NULL,
  `contraseña` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `edad` tinyint(3) UNSIGNED NOT NULL,
  `sexo` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombres`, `apellidos`, `usuario`, `contraseña`, `id_rol`, `edad`, `sexo`) VALUES
(1, 'Marcos', 'Marquez', 'mmarquez', 'Marcos12', 1, 19, 'M'),
(2, 'Emily', 'Mercado', 'memily', 'Emily198', 2, 20, 'F'),
(3, 'Miguel', 'Molinares', 'mmolinares', 'Miguel20', 3, 18, 'M'),
(4, 'Lourdes', 'De Avila', 'Ldavila', 'Admin123', 1, 35, 'F'),
(5, 'Bryan', 'Fernandez', 'bfernandez', 'Admin123', 3, 30, 'M'),
(22, 'ssssss', 'sssss', 'wdwdssss', 'Admin123', 1, 22, 'F'),
(211, 'Emily', 'Mercado', 'Mmercado', 'Admin123', 2, 20, 'F'),
(5959, '55566', 'Villalobos', 'adawdaw', 'Admin123', 1, 22, 'F'),
(12533, 'neymar', 'junior', 'neymarjr', 'Admin123', 1, 21, 'M'),
(51161, 'Miguel', 'fernandez', 'mfernandez', 'Admin123', 3, 22, 'M'),
(55558, 'Andres', 'Lobo', 'landres', 'Admin123', 2, 45, 'M'),
(99898, 'Isabel', 'Villalobos', 'ivillalobobos', 'Admin123', 1, 35, 'F'),
(112333, 'Juan', 'Perez', 'jperez', 'Admin123', 2, 19, 'M'),
(1226889, 'David', 'Molinares', 'mdavid', 'Admin123', 3, 22, 'M');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD PRIMARY KEY (`id_alertas`);

--
-- Indices de la tabla `alertuser`
--
ALTER TABLE `alertuser`
  ADD PRIMARY KEY (`id_alertas`,`id_usuario`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `datos_climaticos`
--
ALTER TABLE `datos_climaticos`
  ADD PRIMARY KEY (`id_dato`),
  ADD KEY `id_galpon` (`id_galpon`);

--
-- Indices de la tabla `galpon`
--
ALTER TABLE `galpon`
  ADD PRIMARY KEY (`id_galpon`);

--
-- Indices de la tabla `granja`
--
ALTER TABLE `granja`
  ADD PRIMARY KEY (`id_granja`);

--
-- Indices de la tabla `gran_galpon`
--
ALTER TABLE `gran_galpon`
  ADD PRIMARY KEY (`id_granja`,`id_galpon`),
  ADD KEY `id_galpon` (`id_galpon`);

--
-- Indices de la tabla `huevos`
--
ALTER TABLE `huevos`
  ADD PRIMARY KEY (`id_recoleccion`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `lote`
--
ALTER TABLE `lote`
  ADD PRIMARY KEY (`id_lote`),
  ADD KEY `id_galpon` (`id_galpon`);

--
-- Indices de la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id_reporte`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_id_lote` (`id_lote`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tareas`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alertas`
--
ALTER TABLE `alertas`
  MODIFY `id_alertas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `datos_climaticos`
--
ALTER TABLE `datos_climaticos`
  MODIFY `id_dato` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `galpon`
--
ALTER TABLE `galpon`
  MODIFY `id_galpon` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `huevos`
--
ALTER TABLE `huevos`
  MODIFY `id_recoleccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `lote`
--
ALTER TABLE `lote`
  MODIFY `id_lote` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id_reporte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_tareas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alertuser`
--
ALTER TABLE `alertuser`
  ADD CONSTRAINT `alertuser_ibfk_1` FOREIGN KEY (`id_alertas`) REFERENCES `alertas` (`id_alertas`),
  ADD CONSTRAINT `alertuser_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `datos_climaticos`
--
ALTER TABLE `datos_climaticos`
  ADD CONSTRAINT `datos_climaticos_ibfk_1` FOREIGN KEY (`id_galpon`) REFERENCES `galpon` (`id_galpon`);

--
-- Filtros para la tabla `gran_galpon`
--
ALTER TABLE `gran_galpon`
  ADD CONSTRAINT `gran_galpon_ibfk_1` FOREIGN KEY (`id_granja`) REFERENCES `granja` (`id_granja`),
  ADD CONSTRAINT `gran_galpon_ibfk_2` FOREIGN KEY (`id_galpon`) REFERENCES `galpon` (`id_galpon`);

--
-- Filtros para la tabla `huevos`
--
ALTER TABLE `huevos`
  ADD CONSTRAINT `huevos_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `lote`
--
ALTER TABLE `lote`
  ADD CONSTRAINT `lote_ibfk_1` FOREIGN KEY (`id_galpon`) REFERENCES `galpon` (`id_galpon`);

--
-- Filtros para la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD CONSTRAINT `fk_id_lote` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`),
  ADD CONSTRAINT `reportes_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
