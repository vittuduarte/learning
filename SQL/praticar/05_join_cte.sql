WITH tb_prim_dia AS (
    SELECT
        DISTINCT IdCliente
        FROM transacoes
        WHERE SUBSTR(dtCriacao, 1, 10) = '2025-08-25'
),

tb_dias_curso AS (
    SELECT
        DISTINCT IdCliente,
        SUBSTR(DtCriacao, 1, 10) AS presenteDia
    FROM transacoes
    WHERE DtCriacao >= '2025-08-25'
    AND DtCriacao < '2025-08-30'
    ORDER BY
        IdCliente,
        presenteDia
),

tb_cliente_dias AS (
    SELECT
        t1.IdCliente,
        COUNT(DISTINCT t2.presenteDia) AS QtdeDias
    FROM tb_prim_dia AS t1
    LEFT JOIN tb_dias_curso AS t2
    ON t1.IdCliente = t2.IdCliente
    GROUP BY t1.IdCliente
)


SELECT
    AVG(QtdeDias)
FROM tb_cliente_dias