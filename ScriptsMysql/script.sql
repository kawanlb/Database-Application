CREATE TABLE genero (
  genero_id INT AUTO_INCREMENT PRIMARY KEY,
  genero_nome VARCHAR(255) NOT NULL
);

CREATE TABLE jogo (
  jogo_id INT AUTO_INCREMENT PRIMARY KEY,
  genero_id INT NOT NULL,
  titulo VARCHAR(255) NOT NULL,
  FOREIGN KEY (genero_id) REFERENCES genero(genero_id)
);

CREATE TABLE editora (
  editora_id INT AUTO_INCREMENT PRIMARY KEY,
  editora_nome VARCHAR(255) NOT NULL
);

CREATE TABLE plataforma (
  plataforma_id INT AUTO_INCREMENT PRIMARY KEY,
  plataforma_nome VARCHAR(255) NOT NULL
);

CREATE TABLE jogo_editora (
  jogo_editora_id INT AUTO_INCREMENT PRIMARY KEY,
  jogo_id INT NOT NULL,
  editora_id INT NOT NULL,
  FOREIGN KEY (jogo_id) REFERENCES jogo(jogo_id),
  FOREIGN KEY (editora_id) REFERENCES editora(editora_id)
);

CREATE TABLE jogo_plataforma (
  jogo_plataforma_id INT AUTO_INCREMENT PRIMARY KEY,
  jogo_editora_id INT NOT NULL,
  plataforma_id INT NOT NULL,
  FOREIGN KEY (jogo_editora_id) REFERENCES jogo_editora(jogo_editora_id),
  FOREIGN KEY (plataforma_id) REFERENCES plataforma(plataforma_id)
);

CREATE TABLE venda (
  venda_id INT AUTO_INCREMENT PRIMARY KEY,
  jogo_plataforma_id INT,
  vendas_na DECIMAL(6,2),
  vendas_eu DECIMAL(6,2),
  vendas_jp DECIMAL(6,2),
  outras_vendas DECIMAL(6,2),
  FOREIGN KEY (jogo_plataforma_id) REFERENCES jogo_plataforma(jogo_plataforma_id)
);