SELECT 
    IdCliente,
    QtdePontos
FROM clientes
ORDER BY QtdePontos DESC
LIMIT 10;

SELECT 
    IdCliente,
    QtdePontos,
    DtCriacao
FROM clientes
ORDER BY DtCriacao, QtdePontos DESC
LIMIT 10;