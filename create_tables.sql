-- Create the "horarios_onibus" table
CREATE TYPE tipo_dia_semana AS ENUM ('dia_util', 'sabado', 'domingo');

CREATE TABLE horarios_onibus (
  id SERIAL PRIMARY KEY,
  id_rota INTEGER REFERENCES rotas(id),
  dia_semana tipo_dia_semana,  -- Usando ENUM
  hora_partida TIMESTAMP,
  hora_chegada TIMESTAMP
);

-- Create the "administradores" table  
CREATE TABLE administradores (
  id SERIAL PRIMARY KEY,
  usuario VARCHAR(50) UNIQUE NOT NULL,
  senha VARCHAR(255) NOT NULL
);

-- Create the "logs" table
CREATE TABLE logs (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  tipo VARCHAR(50), -- Por exemplo: "create", "delete", "update', "error"
  mensagem TEXT, -- Descrição do evento ou erro
  sql_executado TEXT, -- SQL que foi executado
  id_administrador INTEGER REFERENCES administradores(id) -- Para vincular o log ao administrador
);

-- Create the "pontos_trajeto" table
CREATE TABLE pontos_trajeto (
  id SERIAL PRIMARY KEY,
  id_rota INTEGER REFERENCES rotas(id),
  ordem INTEGER NOT NULL,
  latitude DECIMAL(18,14) NOT NULL,
  longitude DECIMAL(18,14) NOT NULL
);

-- Create the "rotas" table
CREATE TABLE rotas (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  nome_variacao VARCHAR(100), -- Nome da variação da rota, se existir
  tipo VARCHAR(10), -- Pode ser "principal" ou "variacao"
  status BOOLEAN DEFAULT TRUE
);

-- Create the "pontos_onibus" table
CREATE TABLE pontos_onibus (
  id SERIAL PRIMARY KEY,
  latitude DECIMAL(18,14) NOT NULL,
  longitude DECIMAL(18,14) NOT NULL,
  link_maps TEXT
);

-- Create the "rotas_ponto_onibus" table
CREATE TABLE rotas_ponto_onibus (
  id SERIAL PRIMARY KEY,
  id_rota INTEGER REFERENCES rotas(id),
  id_ponto_onibus INTEGER REFERENCES pontos_onibus(id),
  ordem INTEGER NOT NULL
);