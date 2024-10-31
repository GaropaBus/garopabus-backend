-- Active: 1730378685587@@garopabus.uk@5432@garopabus@public
-- Inserindo as rotas de ônibus
INSERT INTO rota (nome) VALUES ('Garopaba X Rosa');
INSERT INTO rota (nome) VALUES ('Campo Duna X Garopaba');

-- Inserindo pontos de ônibus para cada rota
-- Pontos de ônibus genéricos (poderão ser ajustados conforme localização e ordem)
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.0, 0.0, 'Ponto Central Garopaba');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.1, 0.1, 'Ponto Praia Rosa');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.2, 0.2, 'Ponto Encantada');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.3, 0.3, 'Ponto Ressacada');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.4, 0.4, 'Ponto Serraria');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.5, 0.5, 'Ponto Central Campo Duna');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.6, 0.6, 'Ponto Lagoa');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.7, 0.7, 'Ponto Pousada Azul');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.8, 0.8, 'Ponto Praia Encantada');
INSERT INTO ponto_onibus (latitude, longitude, nome) VALUES (0.9, 0.9, 'Ponto Alto Rosa');

-- Associando pontos de ônibus com as rotas
-- Exemplo de trajeto para "Garopaba X Rosa"
INSERT INTO ponto_trajeto (id_rota, ordem, latitude, longitude) VALUES 
(1, 1, 0.0, 0.0),
(1, 2, 0.1, 0.1),
(1, 3, 0.2, 0.2),
(1, 4, 0.3, 0.3),
(1, 5, 0.4, 0.4);

-- Exemplo de bifurcações na rota "Garopaba X Rosa"
INSERT INTO bifurcacao (nome, id_rota, id_ponto_inicio, id_ponto_fim) VALUES 
('Ressacada', 1, 3, 4),  -- Bifurcação 1
('Serraria', 1, 4, 5);  -- Bifurcação 2

-- Exemplo de trajeto para "Campo Duna X Garopaba"
INSERT INTO ponto_trajeto (id_rota, ordem, latitude, longitude) VALUES 
(2, 1, 0.5, 0.5),
(2, 2, 0.6, 0.6),
(2, 3, 0.7, 0.7),
(2, 4, 0.8, 0.8),
(2, 5, 0.9, 0.9);

-- Exemplo de bifurcações na rota "Campo Duna X Garopaba"
INSERT INTO bifurcacao (nome, id_rota, id_ponto_inicio, id_ponto_fim) VALUES 
('Encantada', 2, 2, 3),  -- Bifurcação 3
('Lapa', 2, 3, 4);  -- Bifurcação 4

-- Pontos de trajeto para a primeira bifurcação da rota "Garopaba X Rosa" (Ressacada)
INSERT INTO ponto_trajeto_bifurcacao (id_bifurcacao, ordem, latitude, longitude) VALUES
(1, 3.01, 0.21, 0.21),
(1, 3.02, 0.22, 0.22),
(1, 3.03, 0.23, 0.23);

-- Pontos de trajeto para a segunda bifurcação da rota "Garopaba X Rosa" (Encantada)
INSERT INTO ponto_trajeto_bifurcacao (id_bifurcacao, ordem, latitude, longitude) VALUES
(2, 4.01, 0.31, 0.31),
(2, 4.02, 0.32, 0.32),
(2, 4.03, 0.33, 0.33);

-- Pontos de trajeto para a primeira bifurcação da rota "Campo Duna X Garopaba" (Serraria)
INSERT INTO ponto_trajeto_bifurcacao (id_bifurcacao, ordem, latitude, longitude) VALUES
(3, 2.01, 0.61, 0.61),
(3, 2.02, 0.62, 0.62),
(3, 2.03, 0.63, 0.63);

-- Pontos de trajeto para a segunda bifurcação da rota "Campo Duna X Garopaba" (Encantada)
INSERT INTO ponto_trajeto_bifurcacao (id_bifurcacao, ordem, latitude, longitude) VALUES
(4, 3.01, 0.71, 0.71),
(4, 3.02, 0.72, 0.72),
(4, 3.03, 0.73, 0.73);

-- Horários de ônibus para a rota "Garopaba X Rosa"
INSERT INTO horario (id_rota, id_bifurcacao, hora_partida, hora_chegada_prevista) VALUES
(1, 1, '08:00', '08:30'),  -- Partida principal para Ressacada
(1, 2, '08:30', '09:00'),  -- Continuação para Encantada
(1, 1, '10:00', '10:30'),  -- Outro horário para Ressacada
(1, 2, '10:30', '11:00');  -- Continuação para Encantada

-- Horários de ônibus para a rota "Campo Duna X Garopaba"
INSERT INTO horario (id_rota, id_bifurcacao, hora_partida, hora_chegada_prevista) VALUES
(2, 3, '09:00', '09:30'),  -- Partida principal para Serraria
(2, 4, '09:30', '10:00'),  -- Continuação para Encantada
(2, 3, '11:00', '11:30'),  -- Outro horário para Serraria
(2, 4, '11:30', '12:00');  -- Continuação para Encantada



-- SELECT
SELECT 
    r.nome AS nome_rota,
    b.id_bifurcacao,
    b.nome AS nome_bifurcacao,
    h.hora_partida,
    h.hora_chegada_prevista
FROM 
    rota r
JOIN 
    bifurcacao b ON r.id_rota = b.id_rota
LEFT JOIN 
    horario h ON r.id_rota = h.id_rota AND b.id_bifurcacao = h.id_bifurcacao
ORDER BY 
    r.nome, h.hora_partida, b.id_bifurcacao;
