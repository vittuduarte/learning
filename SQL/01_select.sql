SELECT 'Olá mundo!';

SELECT * FROM clientes;

SELECT IdCliente, 
        QtdePontos 
FROM clientes;


SELECT IdCliente, 
        QtdePontos,
        DtCriacao 
FROM clientes
LIMIT 10;