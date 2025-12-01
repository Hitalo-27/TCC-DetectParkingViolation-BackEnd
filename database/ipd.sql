-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 01/12/2025 às 09:09
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

-- --------------------------------------------------------

--
-- Estrutura para tabela `infracoes`
--

CREATE TABLE `infracoes` (
  `id` int NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data` datetime DEFAULT NULL,
  `imagem` varchar(300) NOT NULL,
  `veiculo_id` int NOT NULL,
  `endereco_id` int DEFAULT NULL,
  `tipo_infracao_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Estrutura para tabela `notificacao`
--

CREATE TABLE `notificacao` (
  `id` int NOT NULL,
  `mensagem` varchar(500) NOT NULL,
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int NOT NULL
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
-- Estrutura para tabela `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Despejando dados para a tabela `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `image_url`, `password`) VALUES
(8, 'Shruikan', 'shruikan@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$ZHBCkO14Xq4lgGhcD3KPsu$HCK4UJfzsmcchqcoo/L2eSjaXQXbUBq'),
(9, 'Hitalo Chaves', 'hytalosantos26@gmail.com', '/uploads/user_9_20251123_194214.png', '$bcrypt-sha256$v=2,t=2b,r=12$anYGbwpywH7sfNoOgo6pRu$MK9MarqsiBlZPuxa9s.GLpqh6l/8l.S'),
(11, 'Ryuko', 'ryuko46matoi@gmail.com', '/uploads/user_11_20251123_194603.png', '$bcrypt-sha256$v=2,t=2b,r=12$rm2ksbwnmgrGHZPa/Pqjlu$PRURtkMhmyBDHR3GLM5MINdGjMk61LW'),
(12, 'Giuseppe Cadura', 'ppecadura@gmail.com', '/uploads/user_12_20251125_165006.png', '$bcrypt-sha256$v=2,t=2b,r=12$7EAtInKg.9hqbo7hOI2f6.$4UPvUk5WOB1UOCsha3zxRek.goCkmtO'),
(13, 'Guilherme Abbenante', 'gui2@gmail.com', '/uploads/user_13_20251130_013606.jpg', '$bcrypt-sha256$v=2,t=2b,r=12$weGmH9CBHYiMxWNt.GSu4e$QJASbMy.JmBUyrwJxAMSWv48HxWhPj.'),
(14, 'Guilherme Vieira Abbenante Gomes ', 'gui1@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$w2m3pUSqGINcCySK9Kpbm.$7JZn2EsluYvR7DXzJ2EG4w2gNwp1QXm'),
(15, 'johnjohn', 'johnteste@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$/D0DlOcywPnz9MqFGtBIcu$VclLDQIBhy.LXfkrd8oYePbxLU6ORau'),
(16, 'Josefa', 'josefa@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$7HyZvKdMl7eaedVIg5i6tu$D13qUlRiZpdCuT2nzz9cckBQp8tXH3G'),
(17, 'oioioi', 'oioioi@oi.com', '/uploads/user_17_20251127_230712.jpg', '$bcrypt-sha256$v=2,t=2b,r=12$bE9ESC3Om5rPTgcR2ujYde$GZASaGVAUYgHj7SSwgj9.M4V5B9Vomy'),
(18, 'Paulo', 'paulo@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$5YYA6kVAGQgCNO8PJGzBku$pneERCjQfb36ON/4sYL2iIp7ZdN4C7i'),
(19, 'Guilherme Vieira Abbenante Gomes', 'guixtx@gmail.com', NULL, '$bcrypt-sha256$v=2,t=2b,r=12$8p7PwFWvg5k6HfhYtSnPSO$.JkI0pt5cVQVuucgpp8KXDS2jT7wRI2');

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
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `endereco`
--
ALTER TABLE `endereco`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `infracoes`
--
ALTER TABLE `infracoes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Veiculo` (`veiculo_id`),
  ADD KEY `Tipo Infracao` (`tipo_infracao_id`),
  ADD KEY `Endereco` (`endereco_id`),
  ADD KEY `User` (`user_id`);

--
-- Índices de tabela `notificacao`
--
ALTER TABLE `notificacao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `UserId` (`user_id`);

--
-- Índices de tabela `tipo_infracao`
--
ALTER TABLE `tipo_infracao`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `users`
--
ALTER TABLE `users`
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
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `infracoes`
--
ALTER TABLE `infracoes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT de tabela `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de tabela `veiculo`
--
ALTER TABLE `veiculo`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `infracoes`
--
ALTER TABLE `infracoes`
  ADD CONSTRAINT `Endereco` FOREIGN KEY (`endereco_id`) REFERENCES `endereco` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `Tipo Infracao` FOREIGN KEY (`tipo_infracao_id`) REFERENCES `tipo_infracao` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `User` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `Veiculo` FOREIGN KEY (`veiculo_id`) REFERENCES `veiculo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Restrições para tabelas `notificacao`
--
ALTER TABLE `notificacao`
  ADD CONSTRAINT `UserId` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Restrições para tabelas `veiculo`
--
ALTER TABLE `veiculo`
  ADD CONSTRAINT `veiculo_ibfk_1` FOREIGN KEY (`endereco_id`) REFERENCES `endereco` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
