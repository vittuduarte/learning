SELECT *
FROM transacao_produto AS t1
WHERE t1.Idproduto IN (
	SELECT Idproduto
	FROM produtos
	WHERE DescProduto = 'Resgatar Ponei'
);


SELECT
	COUNT(DISTINCT IdCliente)
FROM transacoes AS t1
WHERE t1.IdCliente IN (
	SELECT DISTINCT IdCliente
	FROM transacoes
	WHERE substr(DtCriacao, 1, 10) = '2025-08-25'
)
AND substr(t1.DtCriacao, 1, 10) = '2025-08-29';



