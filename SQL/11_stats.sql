SELECT
    AVG(QtdePontos) AS mediaPontos,
    ROUND(AVG(QtdePontos), 2) AS mediaPontosArrendodada,
    1 * SUM(QtdePontos) / COUNT(IdCliente) AS mediaCarteiraRoots,
    SUM(FlTwitch),
    SUM(FlEmail)
FROM clientes;