-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 11/12/2025 às 22:58
-- Versão do servidor: 8.0.36
-- Versão do PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `ipd`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `endereco`
--

CREATE TABLE `endereco` (
  `id` int NOT NULL,
  `pais` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `estado` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `cidade` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `rua` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `numero` int DEFAULT NULL,
  `longitude` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `latitude` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `endereco`
--

INSERT INTO `endereco` (`id`, `pais`, `estado`, `cidade`, `rua`, `numero`, `longitude`, `latitude`) VALUES
(1, 'Brasil', 'SP', 'São Paulo', 'Rua Coronel Meireles', 1175, '-46.5360948', '-23.5133711'),
(2, 'Brasil', 'SP', 'FERRAZ DE VASCONCELOS', NULL, NULL, NULL, NULL),
(3, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(4, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(5, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(6, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(7, 'Brasil', 'MG', 'PATOS DE MINAS', NULL, NULL, NULL, NULL),
(8, 'Brasil', 'SP', 'FERRAZ DE VASCONCELOS', NULL, NULL, NULL, NULL),
(9, 'Brasil', 'SP', 'Ferraz de Vasconcelos', 'Avenida Governador Jânio Quadros', NULL, '-46.3849092', '-23.5553479'),
(10, 'Brasil', 'SP', 'SAO PAULO', NULL, NULL, NULL, NULL),
(11, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(12, 'Brasil', 'SP', 'SAO PAULO', NULL, NULL, NULL, NULL),
(13, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(14, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(15, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(16, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(17, 'Brasil', 'SP', 'São Paulo', 'Rua Moreira Neto', NULL, '-46.3926477', '-23.556960500000002'),
(18, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(19, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(20, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(21, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825'),
(22, 'Brasil', 'SP', 'São Paulo', 'Rua Londres', NULL, '-46.5358022', '-23.510825');

-- --------------------------------------------------------

--
-- Estrutura para tabela `infracao`
--

CREATE TABLE `infracao` (
  `id` int NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data` datetime DEFAULT NULL,
  `imagem` varchar(300) NOT NULL,
  `veiculo_id` int NOT NULL,
  `endereco_id` int DEFAULT NULL,
  `tipo_infracao_id` int NOT NULL,
  `usuario_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `infracao`
--

INSERT INTO `infracao` (`id`, `created`, `data`, `imagem`, `veiculo_id`, `endereco_id`, `tipo_infracao_id`, `usuario_id`) VALUES
(1, '2025-12-01 01:12:05', '2025-11-26 17:19:09', '/detect/detec_8bb5fa53-44f2-413f-a2f2-e866b6310ebd.jpg', 1, 1, 1, 19),
(2, '2025-12-01 01:20:46', '2025-11-26 10:39:42', '/detect/detec_a196e16f-571c-4daf-8fd3-426bc339edcf.jpg', 2, 3, 1, 9),
(3, '2025-12-01 01:20:53', NULL, '/detect/detec_533e7b24-94a8-4c96-a9fe-97a0f9c35956.jpg', 3, NULL, 1, 8),
(4, '2025-12-01 01:23:54', '2025-11-26 10:39:42', '/detect/detec_0fb42792-33f5-4daf-b7f3-887afaccc7f4.jpg', 2, 4, 1, 9),
(5, '2025-12-01 01:25:04', '2025-11-26 10:39:42', '/detect/detec_802463ef-debb-4443-8631-80ab4ae3c607.jpg', 2, 5, 1, 9),
(6, '2025-12-01 01:25:30', '2025-11-26 10:39:42', '/detect/detec_e6c1ed0e-3cd0-4d7a-be38-76a084fd294d.jpg', 2, 6, 1, 9),
(7, '2025-12-01 01:26:13', NULL, '/detect/detec_e9aa21fa-29ab-4200-b508-4fe7d2b6a6a1.png', 4, NULL, 2, 9),
(8, '2025-12-01 13:40:14', NULL, '/detect/detec_0c9edabd-fa40-4e39-b824-ca6e98035882.png', 5, NULL, 6, 9),
(9, '2025-12-01 13:48:25', NULL, '/detect/detec_dcf88b63-9fb9-4ac1-bdd7-a33d9ba26805.webp', 6, NULL, 6, 11),
(10, '2025-12-01 13:49:52', '2025-11-26 18:12:26', '/detect/detec_87e86f6a-7d91-4122-916b-f6744d91d04a.jpg', 7, 9, 1, 11),
(11, '2025-12-01 22:02:04', NULL, '/detect/detec_92851382-6268-4f9b-873c-acd2cdc63c5e.png', 8, NULL, 2, 9),
(12, '2025-12-01 22:03:13', NULL, '/detect/detec_8920a59c-e135-4910-8160-2db6acf5ad46.png', 9, NULL, 6, 9),
(13, '2025-12-01 22:05:15', NULL, '/detect/detec_190c59a8-54e4-4094-a1c6-9b81ce1778f4.png', 10, NULL, 2, 9),
(14, '2025-12-01 22:07:13', '2025-11-26 10:39:28', '/detect/detec_b036ce34-809f-4b41-bd72-ec33360d9eb9.jpg', 11, 11, 1, 9),
(15, '2025-12-01 22:08:04', '2025-11-26 17:23:27', '/detect/detec_bf3d6fa2-24c0-4a79-8075-87219b924fab.jpg', 12, 13, 6, 9),
(16, '2025-12-01 22:34:11', '2025-11-26 10:39:28', '/detect/detec_9ae8c8fd-64f5-4ad3-8424-ea26fdd50ba6.jpg', 11, 14, 1, 9),
(17, '2025-12-02 00:12:15', NULL, '/detect/detec_9c4b67e7-14ad-4b1e-af3b-2583f731fca9.png', 13, NULL, 2, 21),
(18, '2025-12-02 00:14:23', '2025-11-26 10:39:28', '/detect/detec_058793e6-294f-465f-b5c3-152a7bba45c3.jpg', 11, 15, 1, 21),
(19, '2025-12-07 23:37:23', '2025-11-26 17:23:27', '/detect/detec_ec99d0af-f3b7-4574-90cd-80e3096fbe3d.jpg', 12, 16, 6, 9),
(20, '2025-12-07 23:39:00', '2025-11-26 10:39:28', '/detect/detec_a9852cac-e8a5-4050-b447-d1502dde77e1.jpg', 11, 17, 1, 9),
(21, '2025-12-08 01:18:16', '2025-11-26 17:23:27', '/detect/detec_9a14713f-f4a4-4536-a111-43a51a2bd4c0.jpg', 12, 21, 6, 9),
(22, '2025-12-08 01:19:20', '2025-11-26 17:23:27', '/detect/detec_b7fcedc3-99a2-475a-9d22-b326c10a223e.jpg', 12, 22, 6, 9);

-- --------------------------------------------------------

--
-- Estrutura para tabela `notificacao`
--

CREATE TABLE `notificacao` (
  `id` int NOT NULL,
  `mensagem` varchar(500) NOT NULL,
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tipo_infracao`
--

CREATE TABLE `tipo_infracao` (
  `id` int NOT NULL,
  `gravidade` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `pontos` int NOT NULL,
  `descricao` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `tipo_infracao`
--

INSERT INTO `tipo_infracao` (`id`, `gravidade`, `pontos`, `descricao`) VALUES
(1, 'Grave', 5, 'Estacionado na Calcada'),
(2, 'Grave', 5, 'Estacionado na Faixa'),
(3, 'Média', 4, 'Obstruindo Garagem'),
(4, 'Média', 4, 'Local Proibido (Guia Amarela)'),
(5, 'Grave', 5, 'Estacionado na Rampa'),
(6, 'Grave', 5, 'Estacionado sob Placa Proibida');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario`
--

CREATE TABLE `usuario` (
  `id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `usuario`
--

INSERT INTO `usuario` (`id`, `username`, `email`, `image_url`, `password`) VALUES
(8, 'Shruikan', 'brunopimentelcityhotmail.com@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$ZHBCkO14Xq4lgGhcD3KPsu$HCK4UJfzsmcchqcoo/L2eSjaXQXbUBq'),
(9, 'Hitalo Chaves', 'hytalosantos26@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$uXkoyHrS1l7GKIeuQ/3hNu$mG/7EzVHxna8IcEv3OgzcjjFjYcWpDe'),
(11, 'Ryuko', 'ryuko46matoi@gmail.com', '/uploads/user_11_20251123_194603.png', '$bcrypt-sha256$v=2,t=2b,r=12$rm2ksbwnmgrGHZPa/Pqjlu$PRURtkMhmyBDHR3GLM5MINdGjMk61LW'),
(12, 'Giuseppe Cadura', 'ppecadura@gmail.com', '/uploads/user_12_20251125_165006.png', '$bcrypt-sha256$v=2,t=2b,r=12$7EAtInKg.9hqbo7hOI2f6.$4UPvUk5WOB1UOCsha3zxRek.goCkmtO'),
(13, 'Guilherme Abbenante', 'gui2@gmail.com', '/uploads/user_13_20251130_013606.jpg', '$bcrypt-sha256$v=2,t=2b,r=12$weGmH9CBHYiMxWNt.GSu4e$QJASbMy.JmBUyrwJxAMSWv48HxWhPj.'),
(14, 'Guilherme Vieira Abbenante Gomes ', 'gui1@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$w2m3pUSqGINcCySK9Kpbm.$7JZn2EsluYvR7DXzJ2EG4w2gNwp1QXm'),
(15, 'johnjohn', 'johnteste@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$/D0DlOcywPnz9MqFGtBIcu$VclLDQIBhy.LXfkrd8oYePbxLU6ORau'),
(16, 'Josefa', 'josefa@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$7HyZvKdMl7eaedVIg5i6tu$D13qUlRiZpdCuT2nzz9cckBQp8tXH3G'),
(17, 'oioioi', 'oioioi@oi.com', '/uploads/user_17_20251127_230712.jpg', '$bcrypt-sha256$v=2,t=2b,r=12$bE9ESC3Om5rPTgcR2ujYde$GZASaGVAUYgHj7SSwgj9.M4V5B9Vomy'),
(18, 'Paulo', 'paulo@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$5YYA6kVAGQgCNO8PJGzBku$pneERCjQfb36ON/4sYL2iIp7ZdN4C7i'),
(19, 'Guilherme Vieira Abbenante Gomes', 'guixtx@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$8p7PwFWvg5k6HfhYtSnPSO$.JkI0pt5cVQVuucgpp8KXDS2jT7wRI2'),
(20, 'Jonas Chaves', 'jonas@gmail.com', '/uploads/user_20_20251201_201433.png', '$bcrypt-sha256$v=2,t=2b,r=12$EZr/Zm8zpZXPDbSjqfd//u$fHI0NowOFYmTDaDMWEVxersQjlWdMJG'),
(21, 'Hitalo', 'hitalochaves27@gmail.com', '/uploads/user_21_20251201_211557.png', '$bcrypt-sha256$v=2,t=2b,r=12$Tau5gxMuODCDuEMv72A1P.$cKVfC6FTnIzP07dkRUazp3BxdWs7SVS'),
(22, 'Teste do Teste ', 'testedoteste@teste.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$UDYmJI4u0T88qCpUQwNqau$cM/Q3sHwnGmNg7Ex8BJq8Ela1IWEhby'),
(23, 'Ervilinha34 ', 'babaquin45@outlook.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$aMF8J/7WYXTfyQg8ZbFdiO$DLQjXAg56PCSb.ndnYNDjx/MG7Q1geK');

-- --------------------------------------------------------

--
-- Estrutura para tabela `veiculo`
--

CREATE TABLE `veiculo` (
  `id` int NOT NULL,
  `cor` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `placa_numero` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `origem` varchar(45) NOT NULL,
  `endereco_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `veiculo`
--

INSERT INTO `veiculo` (`id`, `cor`, `placa_numero`, `origem`, `endereco_id`) VALUES
(1, 'Preta', 'EQG0C81', 'API_Externa', NULL),
(2, 'Vermelha', 'JPY0B31', 'API_Externa', 2),
(3, 'Preta', 'Não Identificada', 'API_Externa', NULL),
(4, 'Cinza Chumbo', 'Não Identificada', 'API_Externa', NULL),
(5, 'Branca', 'PJA2669', 'API_Externa', 7),
(6, 'Vermelha', 'JQZ5330', 'API_Externa', NULL),
(7, 'Vermelha', 'FGJ4F21', 'API_Externa', 8),
(8, 'Cinza Escuro', 'Não Identificada', 'API_Externa', NULL),
(9, 'Prata', 'Não Identificada', 'API_Externa', NULL),
(10, 'Cinza', 'Não Identificada', 'API_Externa', NULL),
(11, 'Prata', 'DAY1267', 'API_Externa', 10),
(12, 'Azul', 'EZX9B48', 'API_Externa', 12),
(13, 'Cinza Escuro', 'Não Identificada', 'API_Externa', NULL);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `endereco`
--
ALTER TABLE `endereco`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `infracao`
--
ALTER TABLE `infracao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Veiculo` (`veiculo_id`),
  ADD KEY `Tipo Infracao` (`tipo_infracao_id`),
  ADD KEY `Endereco` (`endereco_id`),
  ADD KEY `User` (`usuario_id`);

--
-- Índices de tabela `notificacao`
--
ALTER TABLE `notificacao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `UserId` (`usuario_id`);

--
-- Índices de tabela `tipo_infracao`
--
ALTER TABLE `tipo_infracao`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `veiculo`
--
ALTER TABLE `veiculo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `endereco_id` (`endereco_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `endereco`
--
ALTER TABLE `endereco`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de tabela `infracao`
--
ALTER TABLE `infracao`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de tabela `notificacao`
--
ALTER TABLE `notificacao`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tipo_infracao`
--
ALTER TABLE `tipo_infracao`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de tabela `veiculo`
--
ALTER TABLE `veiculo`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `infracao`
--
ALTER TABLE `infracao`
  ADD CONSTRAINT `Endereco` FOREIGN KEY (`endereco_id`) REFERENCES `endereco` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `Tipo Infracao` FOREIGN KEY (`tipo_infracao_id`) REFERENCES `tipo_infracao` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `User` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `Veiculo` FOREIGN KEY (`veiculo_id`) REFERENCES `veiculo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Restrições para tabelas `notificacao`
--
ALTER TABLE `notificacao`
  ADD CONSTRAINT `UserId` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Restrições para tabelas `veiculo`
--
ALTER TABLE `veiculo`
  ADD CONSTRAINT `veiculo_ibfk_1` FOREIGN KEY (`endereco_id`) REFERENCES `endereco` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
