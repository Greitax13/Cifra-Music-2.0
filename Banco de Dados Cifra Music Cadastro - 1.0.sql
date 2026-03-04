drop database cifra_music_cadastro;

create database cifra_music_cadastro;

use cifra_music_cadastro;

CREATE TABLE tb_usuario(
  id INT AUTO_INCREMENT,
  nm_usuario VARCHAR(40),
  nm_login VARCHAR(20),
  ds_senha VARCHAR(32),
  inadmin  ENUM("1","2"),
  CONSTRAINT pk_usuario PRIMARY KEY(id)
);

CREATE TABLE tb_cliente (
    id INT AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    senha_cliente varchar(32),
    id_usuario INT NOT NULL,
    CONSTRAINT pk_clientes PRIMARY KEY (id),
    CONSTRAINT fk_clientes_usuario FOREIGN KEY (id_usuario)
    references tb_usuario (id)
);

INSERT INTO tb_usuario(nm_usuario,nm_login,ds_senha,inadmin)
VALUES ("Administrador","admin","admin",1)