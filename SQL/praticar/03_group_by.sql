-- quantos clientes tem e-mail cadastrado? - [OK]
-- qual cliente juntou mais pontos positivos em 2025-05? - [OK]
-- qual cliente fez mais transações no ano de 2024? - [OK]
-- quantos produtos são de rpg? - [OK]
-- qual o valor médio de pontos positivos por dia? - [OK]
-- qual dia da semana quem tem mais pedidos em 2025? - [Consulta]
-- qual o produto mais transacionado? - [OK]
-- qual o produto com mais pontos transacionado? - [OK]

SELECT
    SUM(FlEmail) AS TotalEmailCadastrados
FROM clientes;

SELECT
    IdCliente,
    SUM(QtdePontos) AS qtdePontosPositivos
FROM transacoes
WHERE DtCriacao >= '2025-05-01' AND DtCriacao < '2025-06-01'
    AND QtdePontos > 0
GROUP BY IdCliente
ORDER BY SUM(QtdePontos) DESC
LIMIT 1;


SELECT
    IdCliente,
    COUNT(DISTINCT IdTransacao),
    strftime('%Y', datetime(substr(DtCriacao, 1, 10))) AS Ano
FROM transacoes
GROUP BY IdCliente
ORDER BY COUNT(IdTransacao) DESC
LIMIT 1;


SELECT
    DescCateogriaProduto,
    COUNT(DescCateogriaProduto)
FROM produtos
WHERE DescCateogriaProduto = 'rpg';


SELECT
    SUM(QtdePontos) AS totalPontos,
    COUNT(DISTINCT substr(DtCriacao, 1, 10)) AS qtdeDiasUnicos,
    SUM(QtdePontos) / COUNT(DISTINCT substr(DtCriacao, 1, 10)) AS MediaPontos
FROM transacoes
WHERE QtdePontos > 0;


SELECT
    strftime('%w', substr(DtCriacao, 1, 10)) AS diaSemana,
    COUNT(IdTransacao) AS QtdeTransacao
FROM transacoes
WHERE substr(DtCriacao, 1,4) = '2025'
GROUP BY diaSemana;

SELECT
    SUM(QtdeProduto) AS qtdeProdutoSoma,
    IdProduto
FROM transacao_produto
GROUP BY IdProduto
ORDER BY qtdeProdutoSoma DESC
LIMIT 1;

SELECT
    SUM(VlProduto * QtdeProduto) AS qtdeProdutoSoma,
    IdProduto
FROM transacao_produto
GROUP BY IdProduto
ORDER BY qtdeProdutoSoma DESC
LIMIT 1;