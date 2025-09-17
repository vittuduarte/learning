--Quais clientes mais perderam pontos por lover?
--Quais clientes assinaram a lista de presença no dia 2025-08-25?
--Do inicio ao fim do nosso curso 2025-08-25 a 2025-08-29, quantos clientes assinaram a lista de presença?
--Clientes mais antigos, tem mais frequência de transação?

SELECT
    t1.IdCliente,
    SUM(t1.QtdePontos) AS pontosPerdidos
FROM transacoes AS t1
LEFT JOIN transacao_produto AS t2 ON t1.IdTransacao = t2.IdTransacao
LEFT JOIN produtos AS t3 ON t2.IdProduto = t3.IdProduto
WHERE DescCateogriaProduto = 'lovers'
GROUP BY t1.IdCliente
ORDER BY SUM(t1.QtdePontos) ASC
LIMIT 10;


SELECT
    t1.IdCliente
FROM transacoes AS t1
LEFT JOIN transacao_produto AS t2 ON t1.IdTransacao = t2.IdTransacao
LEFT JOIN produtos AS t3 ON t2.IdProduto = t3.IdProduto
WHERE t3.DescProduto = 'Lista de presença'
AND substr(t1.DtCriacao, 1, 10) =  '2025-08-25';


SELECT
    COUNT(DISTINCT t1.IdCliente)
FROM transacoes AS t1
LEFT JOIN transacao_produto AS t2 ON t1.IdTransacao = t2.IdTransacao
LEFT JOIN produtos AS t3 ON t2.IdProduto = t3.IdProduto
WHERE t3.DescProduto = 'Lista de presença'
AND t1.DtCriacao >=  '2025-08-25' 
AND t1.DtCriacao < '2025-08-30';


SELECT
    CAST(julianday('now') - julianday(substr(t1.DtCriacao, 1, 19)) AS INTEGER) AS idadeBase,
    COUNT(t2.IdTransacao) AS QtdeTransacoes
FROM clientes AS t1
LEFT JOIN transacoes AS t2 ON t1.IdCliente = t2.IdCliente
GROUP BY 
    t1.IdCliente, 
    idadeBase;
