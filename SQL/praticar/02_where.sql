-- lista de transações com apenas 1 ponto - [OK]
-- lista de pedidos realizados no fim de semana - [OK]
-- lista de clientes com 0 (zero) pontos - [OK]
-- lista de clientes com 100 a 200 pontos (inclusive ambos) - [OK]
-- lista de produtos com nome que começa com "Venda de" - [OK]
-- lista de produtos com nome que terminar com 'lover' - [OK]
-- lista de produtos que são "chapéu" - [OK]
-- lista de transações com o produto "Resgatar Ponei" - [OK]
-- listar todas as transações adicionando uma coluna nova sinalizando 'alto', 'Médio', 'baixo' para o valor dos pontos (<10, <500, >=500) - [OK]

SELECT * 
FROM transacoes
WHERE QtdePontos = 1
LIMIT 20;

SELECT IdTransacao,
        DtCriacao,
        strftime('%w', datetime(substr(DtCriacao, 1, 10))) AS diaSemana
FROM transacoes
WHERE strftime('%w', datetime(substr(DtCriacao, 1, 10))) IN ('0', '6');


SELECT IdCliente, QtdePontos 
FROM clientes
WHERE QtdePontos = 0;


SELECT IdCliente, QtdePontos
FROM clientes
WHERE QtdePontos >= 100 
AND QtdePontos <= 200;


SELECT DescProduto
FROM produtos
WHERE DescProduto LIKE 'Venda de%';


SELECT DescProduto
FROM produtos
WHERE DescProduto LIKE '%Lover';


SELECT DescProduto
FROM produtos
WHERE DescProduto LIKE '%Chapéu%';


SELECT *
FROM transacao_produto
WHERE IdProduto = 15;


SELECT *,
CASE 
    WHEN VlProduto < 10 THEN 'Baixo'
    WHEN VlProduto < 500 THEN 'Médio'
    WHEN VlProduto >= 500 THEN 'Alto'
ELSE 'Valor Null'
END AS nomeValor
FROM transacao_produto;



