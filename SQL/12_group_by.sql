SELECT 
    IdCliente,
    SUM(QtdePontos),
    COUNT(IdTransacao)
FROM transacoes
WHERE DtCriacao >= '2025-07-01' AND DtCriacao < '2025-08-01'
GROUP BY IdCliente
HAVING SUM(QtdePontos) > 4000
ORDER BY IdCliente
LIMIT 10