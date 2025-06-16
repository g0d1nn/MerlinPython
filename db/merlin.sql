-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 24/05/2025 às 03:03
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `merlin`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `assinatura`
--

CREATE TABLE `assinatura` (
  `id_assinatura` int(11) NOT NULL,
  `tipo` varchar(150) NOT NULL,
  `preco` int(11) NOT NULL,
  `descricao` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(11) NOT NULL,
  `nome` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `feedback_jogo`
--

CREATE TABLE `feedback_jogo` (
  `id_feedbackjogo` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_jogo` int(11) DEFAULT NULL,
  `descricao` text DEFAULT NULL,
  `nota` int(11) DEFAULT NULL,
  `data_feedback` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `feedback_video`
--

CREATE TABLE `feedback_video` (
  `id_feedbackvideo` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_videoaula` int(11) DEFAULT NULL,
  `descricao` text DEFAULT NULL,
  `nota` int(11) DEFAULT NULL,
  `data_feedback` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `jogo`
--

CREATE TABLE `jogo` (
  `id_jogo` int(11) NOT NULL,
  `nome` varchar(150) NOT NULL,
  `descricao` varchar(250) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `permissao` enum('padrao','admin') DEFAULT 'padrao',
  `id_assinatura` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `videoaula`
--

CREATE TABLE `videoaula` (
  `id_videoaula` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descricao` varchar(250) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `url_video` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `assinatura`
--
ALTER TABLE `assinatura`
  ADD PRIMARY KEY (`id_assinatura`);

--
-- Índices de tabela `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Índices de tabela `feedback_jogo`
--
ALTER TABLE `feedback_jogo`
  ADD PRIMARY KEY (`id_feedbackjogo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_jogo` (`id_jogo`);

--
-- Índices de tabela `feedback_video`
--
ALTER TABLE `feedback_video`
  ADD PRIMARY KEY (`id_feedbackvideo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_videoaula` (`id_videoaula`);

--
-- Índices de tabela `jogo`
--
ALTER TABLE `jogo`
  ADD PRIMARY KEY (`id_jogo`),
  ADD KEY `fk_jogo_categoria` (`id_categoria`);

--
-- Índices de tabela `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `fk_usuario_assinatura` (`id_assinatura`);

--
-- Índices de tabela `videoaula`
--
ALTER TABLE `videoaula`
  ADD PRIMARY KEY (`id_videoaula`),
  ADD KEY `fk_videoaula_categoria` (`id_categoria`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `assinatura`
--
ALTER TABLE `assinatura`
  MODIFY `id_assinatura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `feedback_jogo`
--
ALTER TABLE `feedback_jogo`
  MODIFY `id_feedbackjogo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `feedback_video`
--
ALTER TABLE `feedback_video`
  MODIFY `id_feedbackvideo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `jogo`
--
ALTER TABLE `jogo`
  MODIFY `id_jogo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `videoaula`
--
ALTER TABLE `videoaula`
  MODIFY `id_videoaula` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `feedback_jogo`
--
ALTER TABLE `feedback_jogo`
  ADD CONSTRAINT `feedback_jogo_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `feedback_jogo_ibfk_2` FOREIGN KEY (`id_jogo`) REFERENCES `jogo` (`id_jogo`);

--
-- Restrições para tabelas `feedback_video`
--
ALTER TABLE `feedback_video`
  ADD CONSTRAINT `feedback_video_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `feedback_video_ibfk_2` FOREIGN KEY (`id_videoaula`) REFERENCES `videoaula` (`id_videoaula`);

--
-- Restrições para tabelas `jogo`
--
ALTER TABLE `jogo`
  ADD CONSTRAINT `fk_jogo_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id_categoria`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Restrições para tabelas `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `fk_usuario_assinatura` FOREIGN KEY (`id_assinatura`) REFERENCES `assinatura` (`id_assinatura`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Restrições para tabelas `videoaula`
--
ALTER TABLE `videoaula`
  ADD CONSTRAINT `fk_videoaula_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id_categoria`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
