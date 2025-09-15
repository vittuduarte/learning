SELECT 
    IdCliente,
    QtdePontos,
CASE
    WHEN QtdePontos <= 500 THEN 'Ponei'
    WHEN QtdePontos <= 1000 THEN 'Ponei Premium'
    WHEN QtdePontos <= 5000 THEN 'Mago Aprendiz'
    WHEN QtdePontos <= 10000 THEN 'Mago Mestre'
    ELSE 'Mago Supremo'
END AS nomeGrupo
FROM clientes
ORDER BY QtdePontos DESC