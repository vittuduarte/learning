--Selecione todos os clientes com e-mail cadastrado
SELECT *
FROM clientes
WHERE FlEmail = 1;
/*
Outras opções
WHERE FlEmail <> 0;
WHERE FlEmail != 0;
*/

--Selecione todas as transações de 50 pontos (exatos)
SELECT *
FROM transacoes
WHERE QtdePontos = 50;

--seleciona todos os clientes com mais de 500 pontos
SELECT *
FROM clientes
WHERE QtdePontos > 500;

--Selecione produtos que contém 'churn' no nome
SELECT *
FROM produtos
WHERE DescProduto LIKE '%churn%';

/*
WHere DescProduto = 'Churn_10pp'
OR DescProduto = 'Churn_2pp'
OR DescProduto = 'Churn_5pp'

WHERE DescProduto IN ('Churn_10pp', 'Churn_5pp', 'Churn_2pp')
*/

