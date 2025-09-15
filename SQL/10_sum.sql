SELECT
    SUM(QtdePontos),
    SUM(CASE WHEN QtdePontos > 0 THEN QtdePontos END) AS qtdePontosPositivos,
    SUM(CASE WHEN QtdePontos < 0 THEN QtdePontos END) AS qtdePontosNegativos,
    COUNT(CASE WHEN QtdePontos < 0 THEN QtdePontos END) AS qtdeTransacoesNegativos
FROM transacoes
WHERE dtCriacao >= '2025-07-01' AND dtCriacao < '2025-08-01'
ORDER BY QtdePontos DESC