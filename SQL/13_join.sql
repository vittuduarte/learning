-- Qual categoria tem mais produtos vendidos?
-- Em 2024, quantas transações de Lovers tivemos?
-- Qual mês tivemos mais listas de presença assinada?
-- Qual o total de pontos trocados na Stream Elements em Jungo de 2025?

SELECT *
FROM transacao_produto AS t1
LEFT JOIN produtos AS t2 ON t1.IdProduto = t2.IdProduto;




SELECT
    t2.DescCateogriaProduto,
    COUNT(DISTINCT t1.IdTransacao) AS QtdeTransacao
FROM transacao_produto AS t1
LEFT JOIN produtos AS t2 ON t1.IdProduto = t2.IdProduto

GROUP BY t2.DescCateogriaProduto
ORDER BY QtdeTransacao DESC;


SELECT
    t1.IdTransacao,
    t1.IdCliente,
    t2.IdProduto,
    t3.DescCateogriaProduto
FROM transacoes AS t1
LEFT JOIN transacao_produto AS t2 ON t1.IdTransacao = t2.IdTransacao
LEFT JOIN produtos AS t3 ON t2.IdProduto = t3.IdProduto
WHERE DtCriacao >='2024-01-01' AND DtCriacao < '2025-01-01'
AND t3.DescCateogriaProduto = 'lovers';



SELECT
     substr(t1.DtCriacao, 1, 7) AS anoMes,
     COUNT(DISTINCT t1.IdTransacao) AS QtdeTransacao
FROM transacoes AS t1
LEFT JOIN transacao_produto AS t2 ON t1.IdTransacao = t2.IdProduto
LEFT JOIN produtos AS t3 ON t2.IdProduto = t3.IdProduto
WHERE DescProduto = 'Lista de presença'
GROUP BY substr(t1.DtCriacao, 1, 7);