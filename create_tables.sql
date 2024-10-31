-- Criação da tabela de Pontos de Ônibus
CREATE TABLE ponto_onibus (
    id_ponto_onibus SERIAL PRIMARY KEY,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    nome VARCHAR(255)
);

-- Criação da tabela de Rotas de Ônibus
CREATE TABLE rota (
    id_rota SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Criação da tabela de Pontos de Trajeto
CREATE TABLE ponto_trajeto (
    id_ponto_trajeto SERIAL PRIMARY KEY,
    id_rota INT NOT NULL REFERENCES rota(id_rota) ON DELETE CASCADE,
    ordem INT NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL
);

-- Criação da tabela de Bifurcações
CREATE TABLE bifurcacao (
    id_bifurcacao SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    id_rota INT NOT NULL REFERENCES rota(id_rota) ON DELETE CASCADE,
    id_ponto_inicio INT NOT NULL REFERENCES ponto_trajeto(id_ponto_trajeto) ON DELETE CASCADE,
    id_ponto_fim INT NOT NULL REFERENCES ponto_trajeto(id_ponto_trajeto) ON DELETE CASCADE
);

-- Criação da tabela de Pontos de Trajeto da Bifurcação
CREATE TABLE ponto_trajeto_bifurcacao (
    id_ponto_bifurcacao SERIAL PRIMARY KEY,
    id_bifurcacao INT NOT NULL REFERENCES bifurcacao(id_bifurcacao) ON DELETE CASCADE,
    ordem DECIMAL(5, 2) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL
);

-- Criação da tabela de Horários de Ônibus
CREATE TABLE horario (
    id_horario SERIAL PRIMARY KEY,
    id_rota INT NOT NULL REFERENCES rota(id_rota) ON DELETE CASCADE,
    id_bifurcacao INT REFERENCES bifurcacao(id_bifurcacao) ON DELETE SET NULL,
    hora_partida TIME NOT NULL,
    hora_chegada_prevista TIME NOT NULL
);

-- Criação da tabela de Horários por Ponto de Ônibus
CREATE TABLE horario_ponto (
    id_horario_ponto SERIAL PRIMARY KEY,
    id_horario INT NOT NULL REFERENCES horario(id_horario) ON DELETE CASCADE,
    id_ponto_onibus INT NOT NULL REFERENCES ponto_onibus(id_ponto_onibus) ON DELETE CASCADE,
    hora_chegada_prevista TIME NOT NULL
);

-- Criação da tabela de relacionamento entre Ponto de Ônibus e Rota (M:N)
CREATE TABLE rota_ponto_onibus (
    id_rota INT NOT NULL REFERENCES rota(id_rota) ON DELETE CASCADE,
    id_ponto_onibus INT NOT NULL REFERENCES ponto_onibus(id_ponto_onibus) ON DELETE CASCADE,
    PRIMARY KEY (id_rota, id_ponto_onibus)
);
